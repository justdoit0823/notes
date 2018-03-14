
package main

import "encoding/json"
import "fmt"
import "io/ioutil"
import "net/http"
import "net/url"
import "os"
import "strings"


type buildingInfo struct {
	ID float64 `json:"ID"`
	NF string `json:"NF"`
	YSXKZH string `json:"YSXKZH"`
	QYMC string `json:"QYMC"`
	XMMC string `json:"XMMC"`
}


type queryResult struct {
	Page int `json:"page"`
	Count int `json:"count"`
	Head []buildingInfo `json:"head"`
}


type noResult struct {
	Page int `json:"page"`
	Count int `json:"count"`
	Head string `json:"head"`
}


func main() {

	if len(os.Args) == 1 {
		fmt.Println("Invalid building name.")
		return
	}

	buildingName := os.Args[1]
	queryUrl := "http://202.103.39.35:9083/WebService1.asmx/SPF_XMMC_KFGSMC_ZH"

	res, err := http.PostForm(queryUrl, url.Values{"xmmc": {buildingName}, "pag": {"1"}})
	if err != nil {
		fmt.Println(err)
		return
	}

	defer res.Body.Close()
	body, err := ioutil.ReadAll(res.Body)

	bodyText := string(body)
	textArray1 := strings.Split(bodyText, "</string>")
	textArray2 := strings.Split(textArray1[0], "{")

	jsonData := "{" + strings.Join(textArray2[1:], "{")

	var result queryResult
	err = json.Unmarshal([]byte(jsonData), &result)
	if err != nil {
		var secondResult noResult
		second_err := json.Unmarshal([]byte(jsonData), &secondResult)
		if second_err != nil {
			fmt.Println(second_err)
		}

		fmt.Println("no result")
		return
	}

	for i := 0; i < result.Count; i++ {
		cell := result.Head[i]
		fmt.Printf("%s %s %s\n", cell.XMMC, cell.QYMC, cell.YSXKZH)
	}

}
