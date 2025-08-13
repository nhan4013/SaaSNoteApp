import React, { useContext, useEffect } from "react"
import AsideBar from "../aside/AsideBar"
import { DataContext } from "../../context";
import {
  Add,
  ArchiveOutlined,
  ArrowBack,
  DeleteOutlineOutlined,
  KeyboardArrowLeft,
  RestartAltOutlined,
  Settings,
} from "@mui/icons-material";
import { useLocation } from "react-router-dom";
import SearchBar from "../page/SearchBar";

function Board() {
    const context = useContext(DataContext);
    if (!context) throw new Error("DataContext not found");
    const {
        notes,
        dispatchNotes,
        searchResults,
        setIsTablet,
        isTablet,
        getContent,
        isDark,
  } = context;

  const archiveData = {
    text:
      notes.asideCurrentTab !== "archivedNotes"
        ? "Archive Note"
        : "Restore Note",
    icon:
      notes.asideCurrentTab !== "archivedNotes"
        ? ArchiveOutlined
        : RestartAltOutlined,
    actionType: "ARCHIVE_NOTE",

    parag:
      notes.asideCurrentTab !== "archivedNotes"
        ? "Are you sure you want to archive this note? You can find it in the Archived Notes section and restore it anytime."
        : "Are you sure you want to restore this note? This note will be restored to All Notes section.",
  };

  const deleteData = {
    text: "Delete Note",
    icon: DeleteOutlineOutlined,
    actionType: "DELETE_NOTE",
    parag:
      "Are you sure you want to delete this note? This action cannot be undone.",
  };

  const newNoteData = {
    text: "Create New Note",
    icon: Add,
    actionType: "SHOW_FORM",
    parag: "",
  };
  const isSettings = notes.asideCurrentTab === "settingsTab";

  useEffect(() => {
    const handleResize = () => setIsTablet(window.innerWidth <= 1200);
    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  const location = useLocation();

    return (
        <div className={`board-wrapper mobile ${isDark && "dark-border"}`}>
            <div className="aside desktop">
                <AsideBar />
            </div>
            <section
        className={`content-wrapper desktop ${isDark && "dark-bl"}`}
        aria-labelledby="main-title"
      >
        <header
          className={`content-header ${isDark && "dark-bb"}`}
          aria-label="Page Header"
        >
          <h1 id="main-title" className="main-title">
            {getContent().title}
          </h1>
          <div className="search-settings-wrapper">
            <SearchBar aria-label="Search Notes" />
            <NavLink
              className={`settings-btn ${isSettings && "active-settings-btn"} ${
                isSettings && isDark && "dark-card-bg"
              }`}
              onClick={() => {
                dispatchNotes({
                  type: "UPDATE_TAB",
                  payload: { tab: "settingsTab", key: "asideCurrentTab" },
                });
              }}
              to={`/settingsTab`}
              aria-label="Settings"
              aria-current={isSettings ? "page" : undefined}
            >
              <Settings
                className={`settings-icon ${isSettings && "current-icon"}`}
                aria-hidden="true"
              />
            </NavLink>
          </div>
        </header>

        {isSettings ? (
          <SettingsPage aria-label="Settings Page" />
        ) : (
          <div className="notes-detailed-wrapper" aria-label="Notes Section">
            <div
              className={`notes-wrapper ${isDark && "dark-br"}`}
              aria-label="Notes List"
            >
              <Button data={newNoteData} aria-label="Create New Note" />
              <p className="main-paragraph" aria-live="polite">
                {getContent().parag}
              </p>

              <NoteCards data={searchResults} aria-label="Search Results" />
            </div>

            <div
              className={`detailed-notes-wrapper ${isDark && "dark-br"}`}
              aria-label="Detailed Notes Section"
            >
              {notes.showForm ? (
                <NoteForm aria-label="Note Form" />
              ) : (
                <DetailedNote aria-label="Detailed Note" />
              )}
            </div>

            {!notes.showForm && (
              <div
                className="btn-actions-wrapper"
                aria-label="Action Buttons Section"
              >
                <Button data={archiveData} aria-label="Archive Notes" />
                <Button data={deleteData} aria-label="Delete Notes" />
              </div>
            )}
          </div>
        )}
      </section>    
        </div>
    )
}

export default Board