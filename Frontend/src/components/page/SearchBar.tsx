import { useContext, useId } from "react";
import { DataContext } from "../../context";
import { SearchOutlined } from "@mui/icons-material";
import NoteCards from "../NoteCard/NoteCards";

function SearchBar() {
  const context = useContext(DataContext);
  if (!context) throw new Error("DataContext not found");
  const { query, setQuery, searchResult, dispatchNotes, isDark, isTablet } =
    context;
  const id = useId();
  return (
    <div className="search-bar mobile" role="search">
      <fieldset
        className={`field ${isDark && "dark-border"}`}
        aria-label="Search notes"
      >
        <SearchOutlined aria-hidden="true" />
        <label htmlFor={id} className="search-label">
          <span className="sr-only">Search for notes</span>
          <input
            type="search"
            value={query}
            onChange={(e) => {
              setQuery(e.target.value);
              dispatchNotes({
                type: "UPDATE_TAB",
                payload: { tab: "searchTab", key: "asideCurrentTab" }
              });
            }}
            className={`search-input ${isDark && "dark-search-input"}`}
            id={id}
            placeholder="Search by title, content, or tags…"
            aria-label="Search by title, content, or tags"
          />
        </label>
      </fieldset>
      {isTablet && (
        <div
          className="search-results"
          role="region"
          aria-label="Search Results"
        >
          <NoteCards data={searchResult} />
        </div>
      )}
    </div>
  );
}

export default SearchBar;
