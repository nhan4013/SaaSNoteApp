import { useContext } from "react";
import { DataContext } from "../../context";
import './NoteCards.css'
import { NavLink, Link } from "react-router-dom";
import { KeyboardArrowLeft } from "@mui/icons-material";
import React from "react";

function NoteCards({ data }) {
  const context = useContext(DataContext);
  if (!context) throw new Error("DataContext not found");
  const { notes, dispatchNotes, isTablet, getContent, isDark } =
    context;
  return (
    <article className="notes-list">
      {isTablet &&
        notes.asideCurrentTab !== "searchTab" &&
        notes.asideCurrentTab === "tags" && (
          <div className="tag-actions-wrapper">
            <Link to="/tags" className="go-back-link tags">
              <KeyboardArrowLeft /> Go Back
            </Link>
            <h2 className={`main-title ${isDark && "dark-text-primary"}`}>
              Notes Tagged : {notes?.currentTag}
            </h2>
            <p className={`main-paragraph ${isDark && "dark-text-secondary"}`}>
              All notes with the '{notes?.currentTag}' tag are shown here.
            </p>
          </div>
        )}
      {isTablet && notes.asideCurrentTab !== "tags" && (
        <>
          <h1 className={`main-title ${isDark && "dark-text-primary"}`}>
            {getContent().title}
          </h1>
          <p className={`main-paragraph ${isDark && "dark-text-secondary"}`}>
            {getContent().parag}
          </p>
        </>
      )}
      {data?.map((note) => {
        const isCurrent = notes?.currentNoteId === note.id;
        const lastEdited = note?.lastEdited;
        const formattedDate = new Date(lastEdited).toLocaleDateString("en-GB", {
          day: "2-digit",
          month: "long",
          year: "numeric",
        });
        return (
          <React.Fragment key={note.id}>
            {isTablet ? (
              <NavLink
                key={note.id}
                className={`note-card ${isDark && "dark-note"}`}
                role="button"
                tabIndex={0}
                onClick={() => {
                  dispatchNotes({
                    type: "UPDATE_NOTE",
                    payload: { id: note?.id },
                  });
                }}
                to="/details"
                aria-label={`Open note: ${note?.title}`}
              >
                <h3 className="note-title">{note?.title}</h3>
                <ul className="card-tag-list" role="list">
                  {note?.tags?.map((tag, i) => (
                    <li
                      key={i}
                      className={`card-tag-item ${isDark && "dark-tag-item"}`}
                      role="listitem"
                    >
                      {tag}
                    </li>
                  ))}
                </ul>
                <p className="card-date">{formattedDate}</p>
              </NavLink>
            ) : (
              <div
                className={`note-card ${isCurrent && "current-note"} ${
                  isDark && "dark-bb"
                } ${isDark && isCurrent && "dark-card-bg"}`}
                role="button"
                tabIndex={0}
                onClick={() => {
                  dispatchNotes({
                    type: "UPDATE_NOTE",
                    payload: { id: note?.id },
                  });
                }}
                aria-label={`Select note: ${note?.title}`}
              >
                <h3 className="note-title">{note?.title}</h3>
                <ul className="card-tag-list" role="list">
                  {note?.tags?.map((tag, i) => (
                    <li
                      key={i}
                      className={`card-tag-item ${isDark && "dark-tag-item"}`}
                      role="listitem"
                    >
                      {tag}
                    </li>
                  ))}
                </ul>
                <p className="card-date">{formattedDate}</p>
              </div>
            )}
          </React.Fragment>
        );
      })}
    </article>
  );
}

export default NoteCards;
