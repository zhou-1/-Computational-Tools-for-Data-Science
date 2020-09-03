https://github.com/gallettilance/CS506-Fall2020/blob/master/00-git/exercises/exercise1.md      
https://github.com/gallettilance/CS506-Fall2020/tree/master/00-git    

1. clone the repo    
```git clone <url_name>```     
2. cd into the repo   
3. ```git remote -v```
4. ```git branch <branch_name>```  --> ```git branch``` to check status    
5. ```touch my-new-file.md``` to create a file    
6. add/stage a file    
```git add my-new-file.md```     
7. commit the file     
```git commit -m 'message'```   
8. push changes
```git push origin <my new branch>```
9.  pull these changes locally    
```git checkout master```    
```git pull origin master```     
Step 15: delete the file    
```rm my-new-file.md ```   
Step 16: recover the file     
```git status```    
Notice that git sees the file was deleted. Undo the change to this file (the change being the deletion)     
```git checkout my-new-file.md```   

