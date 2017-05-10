package main
import (
    "path/filepath"
    "archive/zip"
    "io"
    "os"
    "fmt"
    "flag"
    "regexp"
)

type FileTree struct {
    Root string
    Dest string
    Files []string
    exclude [] *regexp.Regexp
    zipWrite *zip.Writer
    zipFile  *os.File
}

func NewFileTree(src, dest string) *FileTree{
    ft := new(FileTree)
    ft.Root = src
    ft.Dest = dest
    ft.zipFile, _ = os.Create(dest)//need close
    info, _ := ft.zipFile.Stat()
    fName := info.Name()
    println("Create " + fName)
    ft.AddExclude(fName)
    
    ft.zipWrite = zip.NewWriter(ft.zipFile)

    return ft
}

func (self *FileTree)AddExclude(condition string) {
    re := regexp.MustCompile(condition)
    self.exclude = append(self.exclude, re)
}

func (self *FileTree)ZipDir(path string) error {
    err := filepath.Walk(path, func(path string, f os.FileInfo, err error) error {
                
                if ( f == nil ) {return err}

                for _, re := range self.exclude{
                    if re.MatchString(path) {
                        return nil
                    }
                }

                if f.IsDir() { 
                    return nil
                }

                
                println("zip : " + path)
                self.Files = append(self.Files, path)
                self.ZipFile(f, path)
                return nil
        })

    if err != nil {
                fmt.Printf("filepath.Walk() returned %v\n", err)
    }
    return err;
}

func (self * FileTree)ZipFile(info os.FileInfo, fName string) error{
    header, err := zip.FileInfoHeader(info)
    header.Name = fName
    if err != nil {
        return err
    }

    writer, err := self.zipWrite.CreateHeader(header)
    if err != nil {
            return err
    }

    file, err := os.Open(fName)
    _, err = io.Copy(writer, file)
    file.Close()
    return err
}

func (self *FileTree)ZipRoot() error {
    err := self.ZipDir(self.Root)
    return err
}

func (self *FileTree)destory() {
    self.zipWrite.Close()
    self.zipFile.Close()
}

func (self *FileTree)Run() {
    defer self.destory()
    self.ZipRoot()
}

func (self FileTree)Debug() {
    println("=======start debug========")
    for _, fName := range self.Files{
        println(fName)
    }
}

func main(){
        flag.Parse()
        root := flag.Arg(0)
        dest := flag.Arg(1)
        ft := NewFileTree(root, dest)
        ft.AddExclude("unitTest")
        ft.Run()
}
