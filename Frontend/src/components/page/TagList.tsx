import { useContext } from "react";
import { DataContext } from "../../context";
import "../aside/AsideBar.css";
import {
  KeyboardArrowRight,
  LocalOfferOutlined,

} from "@mui/icons-material";
import { Link} from "react-router-dom";


function TagList() {
  const context = useContext(DataContext);
  if (!context) throw new Error("DataContext not found");
  const { notes, dispatchNotes, isDark } = context;
  const tagsList = notes?.notesData.map((obj) => obj.tags);
  const tagsArray = [...new Set(tagsList?.flat())];
  return (
    <ul
      className={`tag-list ${isDark && "dark-tag-list"}`}
      role="list"
      aria-label="List of Tags"
    >
      <li className="tag-heading-item" role="listitem">
        <h3 className={`tag-heading`}>Tags</h3>
      </li>
      {tagsArray.map((tag) => {
        const isCurrent = tag === notes.currentTag;
        return (
          <li
            key={tag}
            className={`tag-item ${isDark && "dark-tag"}`}
            role="listitem"
          >
            <button
              type="button"
              className={`btn desktop ${isCurrent && "current-link"} ${
                isDark && isCurrent && "dark-card-bg"
              }`}
              onClick={() => {
                dispatchNotes({
                  type: "UPDATE_TAB",
                  payload: { tab: "tags", key: "asideCurrentTab" },
                });
                dispatchNotes({ type: "UPDATE_TAG", payload: { tag } });
              }}
              aria-pressed={isCurrent}
              aria-label={`Select tag: ${tag}`}
            >
              <span
                className={`btn-text ${isDark && "dark-text-secondary"}`}
                aria-hidden="true"
              >
                <LocalOfferOutlined
                  className={`tag-icon ${isCurrent && "current-icon"} `}
                />
                {tag}
              </span>
              <span className="sr-only">{`Tag: ${tag}`}</span>
              {isCurrent && <KeyboardArrowRight />}
            </button>
            <Link
              className={`btn mobile ${isDark && "dark-text-secondary"}`}
              to="/filteredTags"
              onClick={() => {
                dispatchNotes({ type: "UPDATE_TAG", payload: { tag } });
                dispatchNotes({
                  type: "UPDATE_TAB",
                  payload: { tab: "tags", key: "asideCurrentTab" },
                });
              }}
              aria-label={`Filter by tag: ${tag}`}
            >
              <LocalOfferOutlined
                className={`tag-icon ${isDark && "dark-text-secondary"}`}
                aria-hidden="true"
              />
              {tag}
            </Link>
          </li>
        );
      })}
    </ul>
  );
}

export default TagList;
