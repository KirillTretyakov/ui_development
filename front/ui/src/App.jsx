import { useState } from "react";

import ResumeUploadPage from "./ResumeUploadPage";
import ResumeMatcherTemplate from "./ResumeMatcherTemplate";

function App() {
  const [matchResult, setMatchResult] = useState(null);

  if (!matchResult) {
    return <ResumeUploadPage onMatchResult={setMatchResult} />;
  }

  return (
    <ResumeMatcherTemplate
      data={matchResult}
      onBack={() => setMatchResult(null)}
    />
  );
}

export default App;