import { useContext, useRef } from "react";
import { Link, useNavigate } from "react-router-dom";
import { DataContext } from "../../context";
import { AccessTimeOutlined, SellOutlined } from "@mui/icons-material";
import './NoteForm.css'
import axios from "axios";
import api from "../../api";

function NoteForm() {
  const context = useContext(DataContext);
 if (!context) throw new Error("DataContext not found");  
  const { notes, dispatchNotes, isTablet, isDark } = context;
  const { title, tags, content } = notes.form;
  const {
    title: validTitle,
    tags: validTags,
    content: validContent,
  } = notes.isValid;

  const navigate = useNavigate();
  const idempotencyKeyRef = useRef<string | null>(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    dispatchNotes({ type: "UPDATE_FORM", payload: { name, value } });
  };
  const handleSubmit = async (e) => {
   
    e.preventDefault();

    if (!idempotencyKeyRef.current) {
      idempotencyKeyRef.current = crypto.randomUUID();
    }
  
    if (validateForm()) {
      try{
        
        await api.post("/notes/",{
          title,
          tags: tags.split(",").map((tag) => tag.trim()),
          content,
          is_archived : false
        },
        {
          headers: {
            "Idempotency-Key": idempotencyKeyRef.current,
          },
        }
      );
        dispatchNotes({ type: "RESET_FORM" });
        idempotencyKeyRef.current = null;
      }catch(error){
        console.error(error)
      }
    } else {
      return;
    }
    
  };

  const validateForm = () => {
    const newFormValid = { ...notes.isValid };
    if (title.trim() === "") {
      newFormValid.title = false;
    }
    if (tags.trim() === "") {
      newFormValid.tags = false;
    }
    if (content.trim() === "") {
      newFormValid.content = false;
    }
    dispatchNotes({
      type: "VALIDATE_FORM",
      payload: { isValid: newFormValid },
    });
    const isValid = Object.values(newFormValid).every(Boolean);
    return isValid;
  };
  return (
    <form className="note-form" aria-labelledby="note-form-title">
      <fieldset className="note-form-field">
        <legend id="note-form-title" className="sr-only">
          Note Form
        </legend>
        <label htmlFor="title" className="title-label">
          <input
            type="text"
            id="title"
            value={title}
            onChange={handleChange}
            name="title"
            placeholder="Enter a title..."
            className={`title-input ${isDark && "dark-title"}`}
            aria-invalid={!validTitle}
            aria-describedby="title-error"
          />
        </label>
        {!validTitle && (
          <span id="title-error" className="error-message">
            Provide a valid title
          </span>
        )}
      </fieldset>

      <div className={`tags-lastEdited-wrapper ${isDark && "dark-bb"}`}>
        <fieldset className="note-form-field">
          <legend className="sr-only">Tags</legend>
          <label htmlFor="tags" className="tag-label">
            <SellOutlined aria-hidden="true" />
            Tags
          </label>
          <input
            type="text"
            id="tags"
            value={tags}
            onChange={handleChange}
            name="tags"
            placeholder="Add tags separated by commas (e.g. Work, Planning)"
            className={`tags-input ${isDark && "dark-tags"}`}
            aria-invalid={!validTags}
            aria-describedby="tags-error"
          />
          {!validTags && (
            <span id="tags-error" className="error-message">
              Provide valid tags
            </span>
          )}
        </fieldset>
        <div className="lastEdited" aria-live="polite">
          <span className="edit-label">
            <AccessTimeOutlined aria-hidden="true" /> Last Edited
          </span>
          <span className="lastEdited-text">Not yet saved</span>
        </div>
      </div>

      <fieldset className={`note-form-field content ${isDark && "dark-bb"}`}>
        <legend className="sr-only">Content</legend>
        <label htmlFor="content" className="content-label">
          
        </label>
        <textarea
          name="content"
          value={content}
          onChange={handleChange}
          id="content"
          className={`textarea-input ${isDark && "dark-content"}`}
          placeholder="Start typing your note here…"
          aria-invalid={!validContent}
          aria-describedby="content-error"
        />
        {!validContent && (
          <span id="content-error" className="error-message">
            Provide valid content!
          </span>
        )}
      </fieldset>

      <fieldset className="form-btn-wrapper">
        <legend className="sr-only">Form Actions</legend>
        {isTablet ? (
          <>
            <Link
              className="form-btn save"
              onClick={handleSubmit}
              to="/"
              role="button"
              aria-label="Save Note"
            >
              Save Note
            </Link>
            <Link
              type="button"
              className="form-btn cancel"
              onClick={() => dispatchNotes({ type: "HIDE_FORM" })}
              to="/"
              role="button"
              aria-label="Cancel"
            >
              Cancel
            </Link>
          </>
        ) : (
          <>
            <button
              type="button"
              className="form-btn save"
              onClick={handleSubmit}
              aria-label="Save Note"
            >
              Save Note
            </button>
            <button
              type="button"
              className="form-btn cancel"
              onClick={() => dispatchNotes({ type: "HIDE_FORM" })}
              aria-label="Cancel"
            >
              Cancel
            </button>
          </>
        )}
      </fieldset>
    </form>
  );
}

export default NoteForm;
