import React, { useContext } from "react";

function AsideBar() {
    return (
        <aside className="aside-wrapper mobile">
            <header className="aside-header desktop">
                <img src={isDark ? logoDark : logo} alt="Notes App logo" className="logo" />
            </header>
            <nav className="aside-nav mobile">
                <ul className="links-wrapper desktop">
                    <TabNav data={headerLinks.slice(0, 2)} tabKey="asideCurrentTab" />
                    <li className="tags-list-item">
                        <TagList />
                    </li>
                </ul>
                <ul className="links-wrapper mobile">
                    <TabNav data={headerLinks} tabKey="asideCurrentTab" />

                </ul>
            </nav>
        </aside>
    )
}

export default AsideBar;