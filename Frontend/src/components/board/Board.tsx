import React from "react"
import AsideBar from "../aside/AsideBar"

function Board() {
    return (
        <div className={`board-wrapper mobile ${isDark && "dark-border"}`}>
            <div className="aside desktop">
                <AsideBar />
            </div>
            
        </div>
    )
}

export default Board