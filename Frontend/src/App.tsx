import { useReducer, useState } from 'react'
import './App.css'

function App() {
  const [notes, dispatchNotes] = useReducer(notesReducer, initialData);

  return (
    <>
      
    </>
  )
}

export default App
