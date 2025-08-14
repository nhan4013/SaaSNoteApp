import { DarkMode, LightMode } from "@mui/icons-material";
import React, { useContext } from "react";
import { motion } from "framer-motion";
import { DataContext } from "../../context";
import { detailedVariants } from "../../variant";
import type { ThemeTab } from "../type/types";

function ThemeOptions() {
  const context = useContext(DataContext);
  if (!context) throw new Error("DataContext not found");
  const { notes, dispatchNotes, isDark } = context;
  const themeData = {
    colorTheme: {
      id: "colorTheme",
      text: "Color Theme",
      parag: "Choose your color theme",
      options: [
        {
          id: "lightMode",
          icon: LightMode,
          label: "Light Mode",
          parag: "Pick a clean and classic light theme"
        },
        {
          id: "darkMode",
          icon: DarkMode,
          label: "Dark Mode",
          parag: "Select a sleek and modern dark theme"
        }
        // {
        //   id: "lightMode",
        //   icon: LightMode,
        //   label: "Light Mode",
        //   parag: "Pick a clean and classic light theme",
        // },
      ]
    },
    fontTheme: {
      id: "fontTheme",
      text: "Font Theme",
      parag: "Choose your font theme:",
      options: [
        {
          id: "'Inter', serif",
          text: "Aa",
          label: "Sans-serif",
          parag: "Clean and modern, easy to read."
        },
        {
          id: "'Noto Serif', serif",
          text: "Aa",
          label: "Serif",
          parag: "Classic and elegant for a timeless feel."
        },
        {
          id: "'Source Code Pro', serif",
          text: "Aa",
          label: "Monospace",
          parag: "Code-like, great for a technical vibe."
        }
      ]
    }
  };
  const obj = themeData[notes.settingsCurrentTab as ThemeTab];
  return (
    <article
      className="theme-options-wrapper"
      role="region"
      aria-labelledby="theme-title"
    >
      <header className="theme-options-header">
        <h3 id="theme-title" className="theme-title">
          {obj.text}
        </h3>
        <p className="theme-parag">{obj.parag}</p>
      </header>
      <ul className="theme-options-list" role="list">
        {obj.options.map((option, index) => {
          const isSelected = option.id === notes[obj.id];
          const isSerif = index === 1;
          const isMono = index === 2;
          return (
            <motion.li
              key={option.id}
              className="theme-option-item"
              role="listitem"
              variants={detailedVariants}
              initial="initial"
              animate="animate"
            >
              <button
                type="button"
                className={`theme-option-btn ${isSelected && "current-theme"} ${
                  isDark && isSelected && "dark-card-bg"
                } ${isDark && "dark-border"}`}
                onClick={() => {
                  dispatchNotes({
                    type: "UPDATE_TAB",
                    payload: {
                      tab: option.id,
                      key: obj.id
                    }
                  });
                }}
                aria-pressed={isSelected}
                aria-label={`Change ${obj.id} to ${option.label}`}
              >
                <span className="left-side-wrapper">
                  <span
                    className={`icon-wrapper ${isDark && "dark-border"}`}
                    aria-hidden="true"
                  >
                    {obj.id === "colorTheme" && "icon" in option ? (
                      <option.icon />
                    ) : "text" in option ? (
                      <span
                        className={`font-option ${isSerif && "serif"} ${
                          isMono && "mono"
                        }`}
                      >
                        {option.text}
                      </span>
                    ) : null}
                  </span>
                  <span className="text-wrapper">
                    <h4 className="option-title">{option.label}</h4>
                    <p className="option-parag">{option.parag}</p>
                  </span>
                </span>
                <span
                  className={`right-icon ${isSelected && "current-icon"}`}
                  aria-hidden="true"
                ></span>
              </button>
            </motion.li>
          );
        })}
      </ul>
    </article>
  );
}

export default ThemeOptions;
