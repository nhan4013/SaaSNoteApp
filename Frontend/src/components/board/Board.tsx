import React from "react"

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