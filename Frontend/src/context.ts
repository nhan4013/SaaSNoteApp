import { createContext } from 'react';
import type { NotesState, Action, Note } from "./components/type/types";

type DataContextType = {
  notes: NotesState;
  dispatchNotes: React.Dispatch<Action>;
  currentNoteObj: Note | undefined;
  searchResult: Note[];
  query: string;
  setQuery: React.Dispatch<React.SetStateAction<string>>;
  isDark: boolean;
  isTablet: boolean;
  setIsTablet: React.Dispatch<React.SetStateAction<boolean>>;
  getContent: () => { title: string; parag: string };
};

export const AppThemeContext = createContext(undefined);
export const DataContext = createContext<DataContextType | undefined>(undefined);

