export interface Note {
  id: string;
  title: string;
  tags: string[];
  content: string;
  lastEdited: string;
  isArchived: boolean;
}

export interface Tag {
  name:string
}

export type NotesState = {
  notesData: Note[];
  asideCurrentTab: string;
  currentNoteId: string | null;
  currentTag: string;
  settingsCurrentTab: string;
  warningModal: boolean;
  showDetailed: boolean;
  modalData: object;
  fontTheme: string;
  colorTheme: string;
  showForm: boolean;
  form: {
    title: string;
    tags: string;
    content: string;
    lastEdited: string;
  };
  isValid: {
    title: boolean;
    tags: boolean;
    content: boolean;
  };
};


export interface ProtectedRouteProps {
  children: React.ReactNode;
  isAuthenticated: boolean;
  redirectTo: string;
}


export type Action =
  | { type: "UPDATE_NOTE"; payload: Note }
  | { type: "ADD_NOTE"; payload: Note }
  | { type: "UPDATE_TAG"; payload: { tag: string } }
  | { type: "DELETE_NOTE"; payload: string } // string = note id
  | { type: "SET_NOTES"; payload: Note[] }
  | { type: "SET_CURRENT_NOTE"; payload: string }; // string = note id