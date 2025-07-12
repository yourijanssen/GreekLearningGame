import Link from "next/link";

export default function Home() {
  return (
    <main style={{ padding: "2rem", maxWidth: 600, margin: "auto" }}>
      <h1>Greek Learning Game 🇬🇷</h1>
      <h2>Beginner</h2>
      <nav style={{ display: "flex", flexDirection: "column", gap: "1rem", margin: "2rem 0" }}>
        <Link href="/alphabet">Alphabet Typing Game</Link>
        <Link href="/numbers">Numbers Typing Game</Link>
        <Link href="/weekdays">Weekdays Typing Game</Link>
        <Link href="/vocabulary">Basic Words Typing Game</Link>
            <Link href="/names">Greek Name Typing Game</Link>
      </nav>
      <h2>Intermediate</h2>
      <nav style={{ display: "flex", flexDirection: "column", gap: "1rem" }}>
        <Link href="/to-be">To be grammer Typing Game</Link>
        <Link href="/phrases">Phrases Typing Game</Link>
        <Link href="/verbs">Verbs Typing Game</Link>
        <Link href="/adjectives">Adjectives Typing Game</Link>
      </nav>
      <h2>Advanced</h2>
      <nav style={{ display: "flex", flexDirection: "column", gap: "1rem" }}>
        <Link href="/sentences">Sentences Typing Game</Link>
        <Link href="/phrases">Phrases Typing Game</Link>
        <Link href="/verbs">Verbs Typing Game</Link>
        <Link href="/adjectives">Adjectives Typing Game</Link>
      </nav>
      <footer style={{ marginTop: "3rem", textAlign: "center", color: "#888" }}>
        <small>Learn Greek by Playing Typing Games!</small> <br /> <br />
        <small>Made by <i>Youri Janssen</i></small>
      </footer>
    </main>
  );
}