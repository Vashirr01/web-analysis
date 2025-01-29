package main

import (
	"encoding/json"
	"log"
	"net/http"
	"os/exec"
	"web-analysis/views" // Update this to match your module name
)

type AnalyzeRequest struct {
	URL string `json:"url"`
}

type ScrapedData struct {
	ScrapedData map[string]interface{} `json:"scraped_data"`
	Summary     string                 `json:"summary"`
}

func main() {
	http.HandleFunc("/", handleIndex)
	http.HandleFunc("/analyze", handleAnalyze)

	log.Println("Server starting on :8080")
	log.Fatal(http.ListenAndServe(":8080", nil))
}

func handleIndex(w http.ResponseWriter, r *http.Request) {
	err := views.index().Render(r.Context(), w)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
	}
}

func handleAnalyze(w http.ResponseWriter, r *http.Request) {
	if r.Method != "POST" {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	url := r.FormValue("url")
	if url == "" {
		http.Error(w, "URL is required", http.StatusBadRequest)
		return
	}

	// Run the Python script with the URL
	cmd := exec.Command("python", "scraper_script.py", url)
	output, err := cmd.Output()
	if err != nil {
		http.Error(w, "Error running scraper: "+err.Error(), http.StatusInternalServerError)
		return
	}

	var result ScrapedData
	err = json.Unmarshal(output, &result)
	if err != nil {
		http.Error(w, "Error parsing scraper output: "+err.Error(), http.StatusInternalServerError)
		return
	}

	err = views.result(result.Summary, result.ScrapedData).Render(r.Context(), w)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
	}
}
