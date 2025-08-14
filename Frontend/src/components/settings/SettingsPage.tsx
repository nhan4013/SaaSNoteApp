import React, { useContext, useEffect } from "react";
import "./Setting.css";
import { DataContext } from "../../context";
import ThemeOptions from "./ThemeOptions";
import { LightMode, TextFields } from "@mui/icons-material";
import TabNav from "../page/TabNav";

function SettingsPage() {
  const context = useContext(DataContext);
  if (!context) throw new Error("DataContext not found");
  const { notes, isTablet, isDark } = context;
  const settingsData = [
    { id: "colorTheme", text: "Color Theme", icon: LightMode },
    { id: "fontTheme", text: "Font Theme", icon: TextFields }
  ];
  useEffect(() => {
    localStorage.setItem("fontTheme", JSON.stringify(notes?.fontTheme));
    localStorage.setItem("colorTheme", JSON.stringify(notes?.colorTheme));
  }, [notes?.fontTheme, notes?.colorTheme]);
  return (
    <div className={`settings-wrapper ${isDark && "dark-bb"}`}>
      {isTablet && <h1 className="main-title settings-title">Settings</h1>}
      <nav className={`settings-nav ${isDark && "dark-br"}`}>
        <ul className="settings-list">
          <TabNav data={settingsData} tabKey="settingsCurrentTab" />
        </ul>
      </nav>
      {isTablet && <div className="divider"></div>}
      <ThemeOptions />
    </div>
  );
}

export default SettingsPage;
