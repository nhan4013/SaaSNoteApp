import React, { useContext } from "react";
import logo from "../../assets/images/logo.svg";
import logoDark from "../../assets/images/logo-dark.png";

function AsideBar() {
    const { notes, dispatchNotes,isDark } = useContext(DataContext)
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