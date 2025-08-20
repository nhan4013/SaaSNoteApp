import React, { useEffect, useRef, useState } from 'react';
import { useParams } from 'react-router-dom';
import * as Y from 'yjs';
import { IndexeddbPersistence } from 'y-indexeddb';
import { QuillBinding } from 'y-quill';
import Quill from 'quill';
import { io } from 'socket.io-client';

class SocketIOProvider {
  private socket: any;
  private doc: Y.Doc;
  private noteId: string;
  private isOnline: boolean = false;
  private messageQueue: any[] = [];

  constructor(socket: any, noteId: string, doc: Y.Doc) {
    this.socket = socket;
    this.doc = doc;
    this.noteId = noteId;

    this.socket.on('connect', () => {
      this.isOnline = true;
      this.socket.emit('join_document', { noteId: this.noteId, user: { name: 'Anonymous' } });
      while (this.messageQueue.length > 0) {
        this.sendUpdate(this.messageQueue.shift());
      }
    });

    this.socket.on('disconnect', () => {
      this.isOnline = false;
    });

    this.socket.on('document_update', (data: any) => {
      if (data.noteId === this.noteId) {
        const update = Uint8Array.from(atob(data.update), c => c.charCodeAt(0));
        Y.applyUpdate(doc, update);
      }
    });

    this.socket.emit('get_document', { noteId: this.noteId }, (response: any) => {
      if (response.updates && response.updates.length) {
        response.updates.forEach((updateStr: string) => {
          const update = Uint8Array.from(atob(updateStr), c => c.charCodeAt(0));
          Y.applyUpdate(doc, update);
        });
      }
    });

    doc.on('update', (update: Uint8Array) => {
      const updateStr = btoa(String.fromCharCode(...update));
      if (this.isOnline) {
        this.sendUpdate(updateStr);
      } else {
        this.messageQueue.push(updateStr);
      }
    });
  }

  private sendUpdate(update: string) {
    this.socket.emit('sync_document', {
      noteId: this.noteId,
      update: update
    });
  }

  destroy() {
    this.socket.emit('leave_document', { noteId: this.noteId });
  }
}

export default function CollaborativeNote() {
  const { noteId } = useParams<{ noteId: string }>();
  const [isLoading, setIsLoading] = useState(true);
  const editorRef = useRef<HTMLDivElement>(null);
  const docRef = useRef<Y.Doc | null>(null);
  const providerRef = useRef<SocketIOProvider | null>(null);

  useEffect(() => {
    if (!noteId || !editorRef.current) return;
    const token = localStorage.getItem('token');
    const socket = io('http://localhost:8000', { auth: { token } });

    const doc = new Y.Doc();
    docRef.current = doc;

    const persistence = new IndexeddbPersistence(`note-${noteId}`, doc);
    persistence.on('synced', () => setIsLoading(false));

    const provider = new SocketIOProvider(socket, noteId, doc);
    providerRef.current = provider;

    const quill = new Quill(editorRef.current, { theme: 'snow' });
    new QuillBinding(doc.getText('content'), quill);

    return () => {
      provider.destroy();
      doc.destroy();
      socket.disconnect();
    };
  }, [noteId,editorRef]);

  setTimeout(() => setIsLoading(false), 2000)

  return (
    <div>
      {isLoading ? (
        <div>Loading editor...</div>
      ) : (
        <div ref={editorRef} style={{ minHeight: 300 }} />
      )}
    </div>
  );
}