package main

import (
	"fmt"

	"github.com/gin-gonic/gin"
	"github.com/jinzhu/gorm"
	_ "github.com/mattn/go-sqlite3"
)

var db *gorm.DB
var err error

type TaskResouce struct {
	ID    int    `gorm:"AUTO_INCREMENT" form:"id" json:"id"`
	Title string `gorm:"not null" form:"title" json:"title"`
	Desc  string `form:"desc" json:"desc"`
	Done  bool   `gorm:"not null default false" form:"done" json:"done"`
}

func Cors() gin.HandlerFunc {
	return func(c *gin.Context) {
		c.Writer.Header().Add("Access-Control-Allow-Origin", "*")
		c.Next()
	}
}

func main() {
	r := gin.Default()
	r.Use(Cors())

	db, err = gorm.Open("sqlite3", "tasks.db")
	if err != nil {
		panic(err)
	}
	defer db.Close()
	db.LogMode(true)
	db.AutoMigrate(&TaskResouce{})

	if err != nil {
		panic(err)
	}

	v1 := r.Group("api/v1")
	{
		v1.POST("/tasks", PostTask)
		v1.GET("/tasks", GetTasks)
		v1.GET("/tasks/:id", GetTask)
		v1.PUT("/tasks/:id", UpdateTask)
		v1.DELETE("/tasks/:id", RemoveTask)
	}
	r.Run(":12306")
}

func PostTask(c *gin.Context) {
	var task TaskResouce
	c.Bind(&task)

	if task.Title != "" {
		db.Create(&task)
		c.JSON(201, gin.H{"success": task})
	} else {
		c.JSON(422, gin.H{"error": "Fields are empty"})
	}
}

func GetTasks(c *gin.Context) {
	var tasks []TaskResouce
	if err := db.Find(&tasks).Error; err != nil {
		c.AbortWithStatus(404)
		fmt.Println(err)
	} else {
		c.JSON(200, tasks)
	}

}

func GetTask(c *gin.Context) {
	id := c.Params.ByName("id")
	var task TaskResouce
	if err := db.Where("id=?", id).First(&task).Error; err != nil {
		c.AbortWithStatus(404)
		fmt.Println(err)
	} else {
		c.JSON(200, task)
	}
}

func UpdateTask(c *gin.Context) {
	var task TaskResouce
	id := c.Params.ByName("id")

	if err := db.Where("id=?", id).First(&task).Error; err != nil {
		c.AbortWithStatus(404)
		fmt.Println(err)
	}
	c.BindJSON(&task)
	db.Save(&task)
	c.JSON(200, task)

}

func RemoveTask(c *gin.Context) {
	var task TaskResouce
	id := c.Params.ByName("id")
	d := db.Where("id=?", id).Delete(&task)
	fmt.Println(d)
	c.JSON(200, gin.H{"id #" + id: "deleted"})
}
