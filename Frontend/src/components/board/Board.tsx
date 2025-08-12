import React, { useContext } from "react"
import AsideBar from "../aside/AsideBar"
import { DataContext } from "../../context";

function Board() {
    const {
        notes,
        dispatchNotes,
        searchResults,
        setIsTablet,
        isTablet,
        getContent,
        isDark,
  } = useContext(DataContext);
    return (
        <div className={`board-wrapper mobile ${isDark && "dark-border"}`}>
            <div className="aside desktop">
                
            </div>
            
        </div>
    )
}

export default Board