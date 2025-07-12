"use client";
import React, { useState, useRef, useEffect } from "react";
import { useRouter } from "next/navigation";

/**
 * Removes diacritics (accents) from a Greek string, for accent-insensitive comparison.
 */
function stripGreekAccents(text: string): string {
  return text
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/ΐ|ΰ/g, (c) => (c === "ΐ" ? "ι" : "υ"));
}

// --- Data
const greekNumbers: [string, string][] = [
  ["1", "ένα"], ["ένα", "1"],
  ["2", "δύο"], ["δύο", "2"],
  ["3", "τρία"], ["τρία", "3"],
  ["4", "τέσσερα"], ["τέσσερα", "4"],
  ["5", "πέντε"], ["πέντε", "5"],
  ["6", "έξι"], ["έξι", "6"],
  ["7", "επτά"], ["επτά", "7"],
  ["8", "οκτώ"], ["οκτώ", "8"],
  ["9", "εννέα"], ["εννέα", "9"],
  ["10", "δέκα"], ["δέκα", "10"],
  ["11", "έντεκα"], ["έντεκα", "11"],
  ["12", "δώδεκα"], ["δώδεκα", "12"],
  ["13", "δεκατρία"], ["δεκατρία", "13"],
  ["14", "δεκατέσσερα"], ["δεκατέσσερα", "14"],
  ["15", "δεκαπέντε"], ["δεκαπέντε", "15"],
  ["16", "δεκαέξι"], ["δεκαέξι", "16"],
  ["17", "δεκαεπτά"], ["δεκαεπτά", "17"],
  ["18", "δεκαοκτώ"], ["δεκαοκτώ", "18"],
  ["19", "δεκαεννέα"], ["δεκαεννέα", "19"],
  ["20", "είκοσι"], ["είκοσι", "20"],
];

// Shuffle Utility
function shuffleArray<T>(array: T[]): T[] {
  const arr = [...array];
  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
  return arr;
}

//---------------- Functional Components ------------------//

/**
 * Reusable stats and timer display
 */
function Stats({ streak, bestStreak, correctCount, total, startTime, finishTime }: {
  streak: number,
  bestStreak: number,
  correctCount: number,
  total: number,
  startTime: number | null,
  finishTime: number | null
}) {
  let display = "";
  if (startTime) {
    const end = finishTime || Date.now();
    const elapsed = Math.floor((end - startTime) / 1000); // sec
    const min = Math.floor(elapsed / 60);
    const sec = elapsed % 60;
    display = `${min > 0 ? min + "m " : ""}${sec < 10 ? "0" : ""}${sec}s`;
  }
  return (
    <div style={{ marginTop: "2.3rem", fontWeight: 500, fontSize: "1.22rem" }}>
      <div>
        Streak: {streak} &nbsp;|&nbsp; Best: {bestStreak} &nbsp;|&nbsp;
        Progress: {correctCount}/{total}
      </div>
      <div style={{ marginTop: "0.5rem", color: "#555" }}>
        Time elapsed: {display}
      </div>
    </div>
  );
}

/**
 * Main in-game view (question, input, buttons, feedback)
 */
function QuizRound({ question, input, onInput, onSubmit, feedback, feedbackColor, inputRef, disabled, onMenu, onListen }: {
  question: string,
  input: string,
  onInput: (e: React.ChangeEvent<HTMLInputElement>) => void,
  onSubmit: (e: React.FormEvent) => void,
  feedback: string | null,
  feedbackColor: string,
  inputRef: React.RefObject<HTMLInputElement | null>,
  disabled: boolean,
  onMenu: () => void,
  onListen: () => void,
}) {
  return (
    <>
      <h2>
  {isNaN(Number(question))
    ? <>Type the <b>number</b> for:</>
    : <>Type the <b>Greek word</b> for:</>
  }
</h2>
      <div
        style={{
          color: "#001e87",
          fontSize: "2.4rem",
          margin: "1.5rem 0",
          fontFamily: "var(--font-geist-mono, monospace)",
        }}
      >
        {question}
      </div>
      <form onSubmit={onSubmit}>
        <input
          ref={inputRef}
          autoFocus
          value={input}
          onChange={onInput}
          placeholder="..."
          style={{
            fontSize: "2rem",
            padding: "0.5rem",
            textAlign: "center",
            width: "110px",
            letterSpacing: "0.075em",
          }}
          disabled={disabled}
        />
        <button
          type="submit"
          style={{ marginLeft: 18, fontSize: "1.15rem", padding: "0.55rem 1.3rem" }}
          disabled={disabled}
        >
          Check
        </button>
        <button
          type="button"
          onClick={onMenu}
          style={{
            marginLeft: 16,
            fontSize: "1.08rem",
            padding: "0.48rem 1.1rem",
            background: "#ddd",
            color: "#333",
            border: "1px solid #aaa",
          }}
          disabled={disabled}
          title="Return to menu"
        >
          Menu
        </button>
        <button
  type="button"
  onClick={onListen}
  style={{
    marginLeft: 16,
    fontSize: "1.08rem",
    padding: "0.48rem 1.1rem",
    background: "#e8f4ff",
    color: "#004d82",
    border: "1px solid #62a0ff",
  }}
  disabled={disabled}
  title="Hear the word in Greek"
>
  Listen
</button>
      </form>
      {feedback && (
        <div
          style={{
            marginTop: "1.6rem",
            color: feedbackColor,
            fontWeight: 600,
            fontSize: "1.15rem",
            minHeight: "2.2em",
          }}
        >
          {feedback}
        </div>
      )}
    </>
  );
}

//---------------- Parent Logic Orchestrator ---------------//

export default function AlphabetGame() {
  // Game state
  const [items, setItems] = useState(() => shuffleArray(greekNumbers));
  const [input, setInput] = useState("");
  const [feedback, setFeedback] = useState<string | null>(null);
  const [streak, setStreak] = useState(0);
  const [bestStreak, setBestStreak] = useState(0);
  const [correctCount, setCorrectCount] = useState(0);
  const [startTime, setStartTime] = useState<number | null>(null);
  const [finishTime, setFinishTime] = useState<number | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  const [log, setLog] = useState<string[]>([]);
  const router = useRouter();

  // Timer start on mount
  useEffect(() => {
    setStartTime(Date.now());
  }, []);

  // Set finishTime when done
  useEffect(() => {
    if (items.length === 0 && finishTime == null) {
      setFinishTime(Date.now());
    }
  }, [items.length, finishTime]);

  useEffect(() => {
  if (!feedback) {
    inputRef.current?.focus();
  }
}, [feedback]);

  // Timer/completion display
  let timeDisplay = "";
  if (startTime && finishTime) {
    const totalSec = Math.floor((finishTime - startTime) / 1000);
    const min = Math.floor(totalSec / 60);
    const sec = totalSec % 60;
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    timeDisplay = `${min > 0 ? min + " min " : ""}${sec < 10 ? "0" : ""}${sec} sec`;
  }

  // Unified feedback color
  const feedbackColor =
    feedback && feedback.startsWith("✅")
      ? "#047c2a"
      : feedback
      ? "#c43219"
      : "";

  // --- Handlers --- //
  function handleInput(e: React.ChangeEvent<HTMLInputElement>) {
    setInput(e.target.value);
  }

  function handleMenu() {
    router.push("/");
  }

  // Auto-return to main menu after finishing the game
useEffect(() => {
  if (items.length === 0 && finishTime != null) {
    const timeout = setTimeout(() => {
      router.push("/");
    }, 1600); // 1.6 seconds delay for feedback, adjust as you like
    return () => clearTimeout(timeout);
  }
}, [items.length, finishTime, router]);

function handleSubmit(e: React.FormEvent) {
  e.preventDefault();
  const [letter, name] = items[0];

  if (stripGreekAccents(input) === stripGreekAccents(letter)) {
    const perfect = input === letter;
    setStreak(s => s + 1);
    setCorrectCount(n => n + 1);
    setBestStreak(now => Math.max(now, streak + 1));
    setItems(arr => shuffleArray(arr.slice(1)));
    // Add new feedback line to log (at the end)
    setLog(prev => [
      perfect
        ? `✅ Correct! Streak: ${streak + 1}`
        : `✅ Correct! The proper way is: ${letter}`,
        ...prev
    ]);
    setInput("");
  } else {
    setLog(prev => [
      `❌ Incorrect! The correct was: ${letter} (${name}). Your streak was: ${streak}`,
    ...prev
    ]);
    setBestStreak(now => Math.max(now, streak));
    setStreak(0);
    setItems(arr => shuffleArray(arr));
    setInput("");
  }
}

function FeedbackLog({ log }: { log: string[] }) {
  return (
    <div style={{
      margin: "1.7rem auto 0",
      maxWidth: 420,
      minHeight: 100,
      background: "#fff8ef",
      border: "1px solid #efb958",
      borderRadius: "7px",
      padding: "1.1rem 1.4rem",
      textAlign: "left",
      fontSize: "1.09rem",
      overflowY: "auto",
      maxHeight: 200
    }}>
      {log.length === 0 ? (
        <span style={{ color: "#969494" }}>Your feedback will appear here...</span>
      ) : (
        <ul style={{ margin: 0, paddingLeft: 18 }}>
          {log.map((msg, i) => (
            <li key={i} style={{ marginBottom: 3 }}>{msg}</li>
          ))}
        </ul>
      )}
    </div>
  )
}


  function handleListen() {
  // This example uses `question` (shown to the user) from your QuizRound props.
  // If you want to read the *letter* instead (from items[0][0]), change accordingly.
  const msg = items[0][0]; // The Greek letter itself
  const utter = new window.SpeechSynthesisUtterance(msg);
  // Try to pick a Greek voice if available
  const voices = window.speechSynthesis.getVoices();
  const greekVoice = voices.find(v => v.lang && v.lang.startsWith("el"));
  if (greekVoice) utter.voice = greekVoice;
  utter.rate = 0.9;
  window.speechSynthesis.speak(utter);
}

  //--------------------- Conditional Routing ---------------------//

return (
  <main style={{ maxWidth: 500, margin: "2rem auto", textAlign: "center" }}>
    {items.length === 0 ? (
      <div>
        <h2>Finished!</h2>
        <div style={{ fontSize: "1.25rem", margin: "2rem 0" }}>
          Well done! You completed the quiz.
        </div>
        {/* Optionally display Stats or a loading spinner */}
      </div>
    ) : (
      <>
        <QuizRound
          question={items[0][1]}
          input={input}
          onInput={handleInput}
          onSubmit={handleSubmit}
          feedback={feedback}
          feedbackColor={feedbackColor}
          inputRef={inputRef}
          disabled={!!feedback}
          onMenu={handleMenu}
          onListen={handleListen}
        />
      </>
    )}
    <FeedbackLog log={log} />
    <Stats
      streak={streak}
      bestStreak={bestStreak}
      correctCount={correctCount}
      total={greekNumbers.length}
      startTime={startTime}
      finishTime={finishTime}
    />
  </main>
);
}