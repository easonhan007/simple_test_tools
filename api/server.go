package main

import (
	"fmt"
	"log"
	"math"
	"net/http"
	"os"
	"time"

	"github.com/appleboy/gin-jwt"
	"github.com/gin-gonic/gin"
)

func helloHandler(c *gin.Context) {
	claims := jwt.ExtractClaims(c)
	c.JSON(200, gin.H{
		"userID": claims["id"],
		"text":   "Hello World.",
	})
}

// User demo
type User struct {
	UserName  string
	FirstName string
	LastName  string
}

func main() {
	port := os.Getenv("PORT")
	r := gin.New()
	r.Use(gin.Logger())
	r.Use(gin.Recovery())

	if port == "" {
		port = "12306"
	}

	// the jwt middleware
	authMiddleware := &jwt.GinJWTMiddleware{
		Realm:      "test zone",
		Key:        []byte("secret key"),
		Timeout:    time.Hour,
		MaxRefresh: time.Hour,
		Authenticator: func(userId string, password string, c *gin.Context) (interface{}, bool) {
			if (userId == "admin" && password == "admin") || (userId == "test" && password == "test") {
				return &User{
					UserName:  userId,
					LastName:  "Bo-Yi",
					FirstName: "Wu",
				}, true
			}

			return nil, false
		},
		Authorizator: func(user interface{}, c *gin.Context) bool {
			if v, ok := user.(string); ok && v == "admin" {
				return true
			}

			return false
		},
		Unauthorized: func(c *gin.Context, code int, message string) {
			c.JSON(code, gin.H{
				"code":    code,
				"message": message,
			})
		},
		// TokenLookup is a string in the form of "<source>:<name>" that is used
		// to extract token from the request.
		// Optional. Default value "header:Authorization".
		// Possible values:
		// - "header:<name>"
		// - "query:<name>"
		// - "cookie:<name>"
		TokenLookup: "header: Authorization, query: token, cookie: jwt",
		// TokenLookup: "query:token",
		// TokenLookup: "cookie:token",

		// TokenHeadName is a string in the header. Default value is "Bearer"
		TokenHeadName: "Bearer",

		// TimeFunc provides the current time. You can override it to use another time value. This is useful for testing or if your server uses a different time zone than your tokens.
		TimeFunc: time.Now,
	}

	r.POST("/login", authMiddleware.LoginHandler)

	// GET
	r.GET("/get/:path", func(c *gin.Context) {
		path := c.Param("path")
		c.JSON(http.StatusOK, gin.H{
			"status": "OK",
			"path":   path,
		})
	})

	r.GET("/get_query", func(c *gin.Context) {
		kw := c.DefaultQuery("keyword", "itest")
		c.JSON(http.StatusOK, gin.H{
			"status":  "OK",
			"keyword": kw,
		})
	})

	// POST
	r.POST("/create_user", func(c *gin.Context) {
		userName := c.PostForm("username")
		password := c.DefaultPostForm("password", "123456")

		c.JSON(http.StatusOK, gin.H{
			"username": userName,
			"password": password,
			"status":   "OK",
		})
	})

	// POST bug[title] bug[desc]
	r.POST("/create_bug", func(c *gin.Context) {
		bug := c.PostFormMap("bug")

		c.JSON(http.StatusOK, gin.H{
			"title":  bug["title"],
			"desc":   bug["desc"],
			"status": "OK",
		})
	})

	r.POST("/upload", func(c *gin.Context) {
		file, _ := c.FormFile("file")
		log.Println(file.Filename)
		c.String(http.StatusOK, fmt.Sprintf("'%s' uploaded"), file.Filename)
	})

	r.GET("/perf_issue", func(c *gin.Context) {
		sum := 0.0
		for i := 1; i < 10000000; i++ {
			sum += math.Sqrt(float64(i))
		}
		c.JSON(http.StatusOK, gin.H{
			"sum":    sum,
			"status": "OK",
		})
	})

	auth := r.Group("/auth")
	auth.Use(authMiddleware.MiddlewareFunc())
	{
		auth.GET("/hello", helloHandler)
		auth.GET("/refresh_token", authMiddleware.RefreshHandler)
	}

	if err := http.ListenAndServe(":"+port, r); err != nil {
		log.Fatal(err)
	}

}
