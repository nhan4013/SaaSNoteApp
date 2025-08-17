import { useEffect, useReducer, useState } from "react";
import "./App.css";
import { data } from "./components/data/data";
import { DataContext } from "./context";
import type { Action, Note, NotesState, Tag } from "./components/type/types";
import { io, type Socket } from "socket.io-client";
import Board from "./components/board/Board";
import axios from "axios";
import { Route, Routes } from "react-router-dom";
import Login from "./components/auth/Login";
import ProtectedRouteProps from "./components/auth/ProtectedRoute";
import { v4 as uuidv4 } from "uuid";
import { isTokenStatus } from "./hooks/useTokenStatus";


const notesReducer = (state: NotesState, action: Action) => {
  switch (action.type) {
    case "UPDATE_NOTE": {
      const { id } = action.payload;
      return {
        ...state,
        currentNoteId: id,
        showDetailed: true
      };
    }
    case "SET_NOTES": {
      const { notes } = action.payload;
      return {
        ...state,
        notesData: Array.isArray(notes) ? notes : [],
        currentNoteId:
          Array.isArray(notes) && notes.length > 0 ? notes[0].id : null
      };
    }

    case "UPDATE_TAG": {
      const { tag } = action.payload;
      return {
        ...state,
        currentTag: tag
      };
    }
    case "UPDATE_TAB": {
      const { tab, key } = action.payload;
      return {
        ...state,
        [key]: tab,
        currentTag: tab === "tags" ? state.currentTag : "",
        showForm: false
      };
    }
    case "OPEN_MODAL": {
      const { modalId, icon, typeText, parag, modalTitle } = action.payload;
      return {
        ...state,
        warningModal: true,
        modalData: { modalId, icon, typeText, parag, modalTitle }
      };
    }
    case "CLOSE_MODAL":
      return {
        ...state,
        warningModal: false,
        modalData: {}
      };
    case "DELETE_NOTE":
      return {
        ...state,
        notesData: state.notesData.filter(
          (note) => note?.id !== state?.currentNoteId
        ),
        warningModal: false,
        modalData: {}
      };
    case "ARCHIVE_NOTE":
      return {
        ...state,
        notesData: state.notesData.map((note) =>
          note.id === state.currentNoteId
            ? {
                ...note,
                isArchived: !note.isArchived
              }
            : note
        ),
        warningModal: false,
        modalData: {}
      };
    case "RESET_FORM":
      return {
        ...state,
        form: { title: "", tags: "", content: "" },
        isValid: { title: true, tags: true, content: true }
      };

    case "SHOW_FORM":
      return {
        ...state,
        showForm: true,
        asideCurrentTab: "allNotes",
        currentTag: ""
      };
    case "HIDE_FORM":
      return {
        ...state,
        showForm: false,
        asideCurrentTab: "allNotes"
      };
    case "UPDATE_FORM": {
      const { name, value } = action.payload;
      return {
        ...state,
        form: {
          ...state.form,
          [name]: value
        },
        isValid: {
          ...state.isValid,
          [name]: true
        }
      };
    }
    case "VALIDATE_FORM": {
      const { isValid } = action.payload;
      return {
        ...state,
        isValid: {
          ...isValid
        }
      };
    }
    case "CREATE_NOTE": {
      const { title, tags, content, lastEdited } = action.payload;
      return {
        ...state,
        notesData: [
          { id: uuidv4(), title, tags, lastEdited, content, isArchived: false },
          ...state.notesData
        ],
        showForm: false,
        form: {
          title: "",
          tags: "",
          content: "",
          lastEdited: ""
        },
        isValid: {
          title: true,
          tags: true,
          content: true
        }
      };
    }
    case "EDIT_NOTE": {
      const {
        editNoteId,
        title: editTitle,
        tags: editTags,
        content: editContent,
        lastEdited: newData
      } = action.payload;
      return {
        ...state,
        notesData: state.notesData.map((note) =>
          note.id === editNoteId
            ? {
                ...note,
                title: editTitle,
                tags: editTags,
                content: editContent,
                lastEdited: newData
              }
            : note
        ),
        currentNoteId: editNoteId
      };
    }
    case "TOGGLE_DETAILS_PAGE": {
      return {
        ...state,
        showDetailed: false
      };
    }

    default:
      return state;
  }
};

function App() {
  const [savedData, setSavedData] = useState<Note[]>([]);
  const [TagsData, setTagsData] = useState<Tag[]>([]);

  const api = axios.create({
    baseURL: "http://localhost:8000"
  });

  const refreshAccessToken = async () => {
    const refresh = localStorage.getItem("refresh_token");
    if (!refresh) return null;
    try {
      const response = await axios.post(
        "http://127.0.0.1:8001/auth/token/refresh",
        { refresh }
      );
      const { access } = response.data;
      localStorage.setItem("access_token", access);
      return access;
    } catch (err) {
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
      window.location.href = "/login";
      return null;
    }
  };

  api.interceptors.request.use(
    async (config) => {
      let token = localStorage.getItem("access_token");

      if (isTokenStatus(token)) {
        token = await refreshAccessToken();
      }
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    },
    (error) => {
      return Promise.reject(error);
    }
  );
    const isAuthenticated = () => {
      return localStorage.getItem("access_token") !== null;
  }

  useEffect(() => {
    if (!isAuthenticated()) return;
    console.log(!isAuthenticated())
    api
      .get("/notes/")
      .then((res) => {
        setSavedData(res.data);
        dispatchNotes({ type: "SET_NOTES", payload: { notes: res.data } });
        console.log(res.data);
      })
      .catch((err) => console.log("Failed to fetch notes:", err));
  }, []);

  useEffect(() => {
    const socket: Socket = io("http://localhost:8000", {
      transports: ["websocket"],
      auth(cb) {
        cb({ token: localStorage.getItem("access_token") });
      }
    });

    socket.on("connect", () => {
      console.log("Connected to Socket.IO server");
    });

    socket.on("notes_update", (data) => {
      console.log("update notes");
      setSavedData(JSON.parse(data));
      dispatchNotes({ type: "SET_NOTES", payload: { notes: JSON.parse(data) } });
    });

    socket.on("tags_update", (data) => {
      setTagsData(JSON.parse(data));
    });

    socket.on("token_expired", async (data) => {
      const refresh = localStorage.getItem("refresh_token");
      if (refresh) {
        try {
          const response = await axios.post(
            "http://127.0.0.1:8001/auth/token/refresh",
            { refresh }
          );
          const { access } = response.data;
          localStorage.setItem("access_token", access);
          socket.auth = { token: access };
          socket.connect();
          axios
            .get("http://localhost:8000/notes/", {
              headers: {
                Authorization: `Bearer ${access}`
              }
            })
            .then((res) => setSavedData(res.data))
            .catch((err) => console.log("Failed to fetch notes:", err));
        } catch (err) {
          console.log(err);
          localStorage.removeItem("access_token");
          localStorage.removeItem("refresh_token");
          window.location.href = "/login";
        }
      } else {
        window.location.href = "/login";
      }
    });

    socket.on("disconnect", () => {
      console.log("Disconnected from Socket.IO server");
    });

    return () => {
      socket.disconnect();
    };
  }, []);

  const initialData = {
    notesData: savedData.length > 0 ? savedData : data,
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
    fontTheme: JSON.parse(
      localStorage.getItem("fontTheme") || '"Inter, serif"'
    ),
    colorTheme: JSON.parse(localStorage.getItem("colorTheme") || '"lightMode"'),
    showForm: false,
    form: {
      title: "",
      tags: "",
      content: "",
      lastEdited: ""
    },
    isValid: {
      title: true,
      tags: true,
      content: true
    }
  };
  const [notes, dispatchNotes] = useReducer(notesReducer, initialData);
  const [query, setQuery] = useState("");
  const [isTablet, setIsTablet] = useState(window.innerWidth <= 1200);

  const filterData = notes?.notesData?.filter((note: Note) => {
    if (notes?.asideCurrentTab === "archivedNotes") {
      return note?.isArchived;
    }
    if (notes?.asideCurrentTab === "tags") {
      return note?.tags?.includes(notes.currentTag) && !note.isArchived;
    } else {
      return !note?.isArchived;
    }
  });

  const searchResult = filterData?.filter(
    (note: Note) =>
      note?.title.toLowerCase().includes(query?.toLowerCase()) ||
      note?.tags.some((tag) => tag.toLowerCase().includes(query.toLowerCase()))
  );

  const currentNoteObj = searchResult?.find(
    (note: Note) => note?.id === notes?.currentNoteId
  );

  useEffect(() => {}, [searchResult, notes?.currentNoteId]);
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
    <DataContext.Provider
      value={{
        notes,
        dispatchNotes,
        currentNoteObj,
        searchResult,
        query,
        setQuery,
        isDark,
        isTablet,
        setIsTablet,
        getContent
      }}
    >
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route
          path="/*"
          element={
            <ProtectedRouteProps
              isAuthenticated={isAuthenticated()}
              redirectTo="/login"
            >
              <main
                className={`outer-container ${isDark && "dark-body-bg"}`}
                style={{ fontFamily: `${notes.fontTheme}` }}
              >
                <Board />
              </main>
            </ProtectedRouteProps>
          }
        />
      </Routes>
    </DataContext.Provider>
  );
}

export default App;
