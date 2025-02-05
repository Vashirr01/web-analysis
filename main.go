package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"github.com/a-h/templ"
	"github.com/gin-gonic/gin"
	"log"
	"net/http"
	"os/exec"
)

type AnalyzeRequest struct {
	URL string `json:"url"`
}

type ScrapedData struct {
	ScrapedData []map[string]interface{} `json:"scraped_data"` // Change to slice of maps
	Summary     string                   `json:"summary"`
}

func templRender(c *gin.Context, status int, component templ.Component) error {
	c.Status(status)
	return component.Render(c.Request.Context(), c.Writer)
}

func main() {
	// Enable detailed logging
	gin.SetMode(gin.DebugMode)
	r := gin.Default()

	r.GET("/", func(c *gin.Context) {
		if err := templRender(c, http.StatusOK, Index()); err != nil {
			log.Printf("Error rendering index: %v", err)
			c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		}
	})

	r.POST("/analyze", func(c *gin.Context) {
		url := c.PostForm("url")
		if url == "" {
			log.Print("URL is empty")
			c.JSON(http.StatusBadRequest, gin.H{"error": "URL is required"})
			return
		}

		log.Printf("Attempting to analyze URL: %s", url)

		// Create command with stdout and stderr capture
		cmd := exec.Command("python", "scraper_script.py", url)
		var stdout, stderr bytes.Buffer
		cmd.Stdout = &stdout
		cmd.Stderr = &stderr

		// Run the command
		err := cmd.Run()
		if err != nil {
			errMsg := fmt.Sprintf("Error running scraper: %v\nStderr: %s", err, stderr.String())
			log.Print(errMsg)
			c.JSON(http.StatusInternalServerError, gin.H{"error": errMsg})
			return
		}

		// Log the Python script output
		log.Printf("Python script output: %s", stdout.String())

		// Try to parse the output
		var result ScrapedData
		if err := json.Unmarshal(stdout.Bytes(), &result); err != nil {
			errMsg := fmt.Sprintf("Error parsing scraper output: %v\nOutput: %s", err, stdout.String())
			log.Print(errMsg)
			c.JSON(http.StatusInternalServerError, gin.H{"error": errMsg})
			return
		}

		// Check if we got valid data
		if result.ScrapedData == nil {
			log.Print("Scraped data is nil")
			c.JSON(http.StatusInternalServerError, gin.H{"error": "No data returned from scraper"})
			return
		}

		// Render the result
		if err := templRender(c, http.StatusOK, Result(result.Summary, result.ScrapedData)); err != nil {
			log.Printf("Error rendering result: %v", err)
			c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		}
	})

	log.Println("Server starting on :8080")
	log.Fatal(r.Run(":8080"))
}
