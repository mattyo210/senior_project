# senior_project
## Usage
### or create a new repository on the command line　　
echo "# senior_project" >> README.md  
git init  
git add README.md  
git commit -m "first commit"    
git remote add origin git@github.com:mattyo210/senior_project.git    
git push -u origin master  
### …or push an existing repository from the command line
git remote add origin git@github.com:mattyo210/senior_project.git  
git push -u origin master  
### …or import code from another repository
You can initialize this repository with code from a Subversion, Mercurial, or TFS project.

### Arigataimemo
1回目  
git clone (clone   のhttps::…..)       Clone or Downloadのやつ  
するとそのディレクトリごとDLできる  

２回目以降  
git pull  (最新状態にする）  
以下：ブランチ名を”test”とする。適宜変えること。  

git checkout -b test

===testブランチで編集===

git add .  
git commit -m “white change”  

git push origin test  

ここで  
git  checkout master  
ここまでで各自の修正や、開発は終わり。  
GitHubの該当プロダクトURLへ飛ぶ’  

その中でPull requrestを選択  
New pull requestを選択  

そのページでpushされたブランチ名を選択できるから自分のブランチ名を選択して  
Create pull request を選択。（ここで変更内容を記載するフォームある）  

そしたらプロダクト主（３人揃った時にみんなでもいいし、少なからず自分でない誰か）がその pull request されたブランチをローカルで試す。　　　以下それの手段


git fetch origin pull/番号/head:test

とするとあなたの作業ディレクトリに該当ブランチが作られるため  
git checkout test  
をし、動作確認をすること  

その後    
git checkout master  

をし、mergeして良さそうならプロダクトページに戻って、  
Merge pull requestを行うことで GitHub  の中身が変更される。  

この際に自分もgit pull をしておくことを忘れない。  
 

どんな時でもgit checkout -b newBranch  
をするときはその直前にgit pullを忘れてはいけない！！！！  
