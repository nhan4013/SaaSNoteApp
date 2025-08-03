import { useEffect, useReducer, useState } from 'react'
import './App.css'
import { data } from './components/data/data';
import { AppThemeContext, DataContext } from './components/contexts';
import type { Note } from './components/type/types';


function App() {
  const savedData: string | null = localStorage.getItem("notes");
  const parsedData : Note[] | null = savedData ? JSON.parse(savedData) : null;


  const initialData = {
    notesData: parsedData ? parsedData : data,
    asideCurrentTab: "allNotes",
    currentNoteId:
      parsedData && parsedData?.length > 0
        ? parsedData?.[0].id
        : data?.length > 0
          ? data[0].id
          : null,
    currentTag: "",
    settingsCurrentTab: "colorTheme",
    warningModal: false,
    showDetailed: false,
    modalData: {},
    fontTheme:
      JSON.parse(localStorage.getItem("fontTheme")) || "'Inter', serif",
    colorTheme: JSON.parse(localStorage.getItem("colorTheme")) || "lightMode",
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
    () => {
      localStorage.setItem('notes', JSON.stringify(notes?.notesData))
    }, [notes?.notesData]
  );

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
