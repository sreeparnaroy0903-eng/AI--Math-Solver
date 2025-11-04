document.getElementById("solve-btn").addEventListener("click", async () => {
  const problemType = document.getElementById("problem-type").value;
  const problemInput = document.getElementById("problem-input").value.trim();
  const resultBox = document.getElementById("result");
  
  if (!problemInput) {
    resultBox.innerHTML = "⚠️ Please enter a math problem first!";
    return;
  }

  resultBox.innerHTML = "⏳ Calculating...";

  try {
    const response = await fetch("https://ai-math-solver-5hg4.onrender.com/solve", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        type: problemType,
        expression: problemInput
      })
    });

    if (!response.ok) {
      throw new Error("Server error: " + response.status);
    }

    const data = await response.json();

    if (data.steps && Array.isArray(data.steps)) {
      // Show step-by-step explanation with typing animation
      resultBox.innerHTML = "";
      for (let i = 0; i < data.steps.length; i++) {
        await new Promise(resolve => setTimeout(resolve, 600));
        resultBox.innerHTML += `<div>${data.steps[i]}</div>`;
      }
      resultBox.innerHTML += `<div style="margin-top:10px; font-weight:bold;">✅ Final Result: ${data.result.replaceAll("**", "^")}</div>`;
    } else {
      resultBox.innerHTML = `<div>✅ Result: ${data.result.replaceAll("**", "^")}</div>`;
    }

  } catch (error) {
    console.error(error);
    resultBox.innerHTML = "❌ Error: Could not connect to the server. Please try again later.";
  }
});
