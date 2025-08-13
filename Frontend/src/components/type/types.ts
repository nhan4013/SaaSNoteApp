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
  | { type: "UPDATE_NOTE"; payload: { id: string } }
  | { type: "UPDATE_TAG"; payload: { tag: string } }
  | { type: "UPDATE_TAB"; payload: { tab: string; key: string } }
  | { type: "OPEN_MODAL"; payload: { modalId: string; icon: string; typeText: string; parag: string; modalTitle: string } }
  | { type: "CLOSE_MODAL" }
  | { type: "DELETE_NOTE" }
  | { type: "ARCHIVE_NOTE" }
  | { type: "SHOW_FORM" }
  | { type: "HIDE_FORM" }
  | { type: "UPDATE_FORM"; payload: { name: string; value: string } }
  | { type: "VALIDATE_FORM"; payload: { isValid: { title: boolean; tags: boolean; content: boolean } } }
  | { type: "CREATE_NOTE"; payload: { title: string; tags: string[]; content: string; lastEdited: string } }
  | { type: "EDIT_NOTE"; payload: { editNoteId: string; title: string; tags: string[]; content: string; lastEdited: string } }
  | { type: "TOGGLE_DETAILS_PAGE" };


  