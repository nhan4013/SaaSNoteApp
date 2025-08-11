import { useEffect, useReducer, useState } from 'react'
import './App.css'
import { data } from './components/data/data';
import {DataContext} from './context';
import type { Action, Note,NotesState,Tag } from './components/type/types';
import { io, type Socket } from 'socket.io-client';

const notesReducer = (state:NotesState,action:Action) => {
  switch(action.type){
    case "UPDATE_NOTE":
      { const { id } = action.payload;
      return {
        ...state,
        currentNoteId :id ,
        showDetailed : true
      }; }
    case "UPDATE_TAG":
      { const { tag } = action.payload;
      return {
        ...state,
        currentTag: tag,
      }; }
    default :
      return state; 
  }
}

function App() {
  const [savedData, setSavedData] = useState<Note[]>([]);
  const [TagsData, setTagsData] = useState<Tag[]>([])

  useEffect(
    () => {
     const socket:Socket = io("http://localhost:8000",{
      transports:["websocket"]
     });

     socket.on("connect",()=>{
      console.log("Connected to Socket.IO server")
     });

     socket.on("notes_update", (data) => {
      setSavedData(JSON.parse(data))
     });

     socket.on("tags_update",(data)=>{
      setTagsData(JSON.parse(data))
     })

     socket.on("disconnect",()=>{
      console.log("Disconnected from Socket.IO server");
     });

     return () =>{
      socket.disconnect();
     };
    },[]
  );



  const initialData = {
    notesData: savedData ? savedData : data,
    asideCurrentTab: "allNotes",
    currentNoteId:
      savedData && savedData?.length > 0
        ? savedData?.[0].id
        : data?.length > 0
          ? data[0].id
          : null,
    currentTag: "",
    settingsCurrentTab: "colorTheme",
    warningModal: false,
    showDetailed: false,
    modalData: {},
    fontTheme:
      JSON.parse(localStorage.getItem("fontTheme") || "'Inter', serif"),
    colorTheme: JSON.parse(localStorage.getItem("colorTheme") || "lightMode"),
    showForm: false,
    form: {
      title: "",
      tags: "",
      content: "",
      lastEdited: "",
    },
    isValid: {
      title: true,
      tags: true,
      content: true,
    },
  };
  const [notes, dispatchNotes] = useReducer(notesReducer, initialData);
  const [query, setQuery] = useState("");
  const [isTablet, setIsTablet] = useState(window.innerWidth <= 1200);

  const filterData = notes?.notesData?.filter(
    (note: Note) => {
      if (notes?.asideCurrentTab === "archivedNotes") {
        return note?.isArchived;
      }
      if (notes?.asideCurrentTab === "tags") {
        return note?.tags?.includes(notes.currentTag) && !note.isArchived;
      }
      else {
        return !note?.isArchived;
      }
    }
  )

  const searchResult = filterData?.filter(
    (note: Note) =>
      note?.title.toLowerCase().includes(query?.toLowerCase()) ||
      note?.tags.some((tag) => tag.toLowerCase().includes(query.toLowerCase()))
  )

  const currentNoteObj = searchResult?.find(
    (note:Note) => note?.id === notes?.currentNoteId
  );


  useEffect(
    ()=>{
      
    },[searchResult,notes?.currentNoteId]
  )
  const isDark = notes.colorTheme === "darkMode";

  const getContent = () => {
    let title = "";
    let parag = "";
    if (notes.asideCurrentTab === "allNotes") {
      title = "All Notes";
    }
    if (notes.asideCurrentTab === "archivedNotes") {
      title = "Archived Notes";
      parag =
        "All your archived notes are stored here. You can restore or delete them anytime.";
    }
    if (notes.asideCurrentTab === "tags") {
      title = `Notes Tagged: ${notes.currentTag}`;
      parag = `All notes tagged with '${notes.currentTag}' are stored here.`;
    }
    if (notes.asideCurrentTab === "searchTab") {
      title = `Search`;
      parag = `All notes matching "${query}" are displayed here.`;
    }
    if (notes.asideCurrentTab === "settingsTab") {
      title = "Settings";
    }
    return { title, parag };
  };

  return (
    <DataContext.Provider value={{
      notes,
      dispatchNotes,
      currentNoteObj,
      searchResult,
      query,
      setQuery,
      isDark,
      isTablet,
      setIsTablet,
      getContent,
    }}>

    </DataContext.Provider>
  )
}

export default App
