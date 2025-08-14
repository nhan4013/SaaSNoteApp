import React, { useContext } from "react";
import logo from "../../assets/images/logo.svg";
import logoDark from "../../assets/images/logo-dark.png";
import "./AsideBar.css";
import { DataContext } from "../../context";
import TabNav from "../page/TabNav";
import { ArchiveOutlined, HomeOutlined, LocalOfferOutlined, Search, Settings } from "@mui/icons-material";
import TagList from "../page/TagList";

function AsideBar() {
    const context = useContext(DataContext);
    if (!context) throw new Error("DataContext not found");
    const { notes, dispatchNotes,isDark } = context
    const headerLinks = [
    { id: "allNotes", url:"/", text: "All Notes", icon: HomeOutlined },
    { id: "archivedNotes", url:"/archivedNotes", text: "Archived Notes", icon: ArchiveOutlined },
    { id: "tags", url:"/tags", text: "Tags", icon: LocalOfferOutlined },
    { id: "searchTab", url:"/searchTab", text: "Search", icon: Search },
    { id: "settingsTab", url:"/settingsTab", text: "Settings", icon: Settings },
  ];

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