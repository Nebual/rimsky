rimsky
======

CST2013 Fiddlings

SVN Basics:
-----------

Create a Github account and tell me it so I can grant you permissions  
  
-- Install an SVN client --  
For Windows, [TortoiseSVN](http://tortoisesvn.net/downloads.html) is a nice GUI with a right click menu in explorer, and comes with commandline SVN tools too.  
For Linux, ```sudo apt-get install subversion```  
  
-- Checkout this repository: --  
In TortoiseSVN, right click your documents folder -> SVN Checkout, and enter https://github.com/Nebual/rimsky as the url.  
CLI: ```svn checkout https://github.com/Nebual/rimsky```  
  
You now have the latest files! They're in rimsky/trunk/  
  
-- To Update (get the latest changes by other people): --  
TortoiseSVN: Right click trunk -> TortoiseSVN -> Update  
CLI: ```svn update``` or ```svn up```  
  
-- To commit (save and upload) your changes: --  
TortoiseSVN: Right click trunk -> TortoiseSVN -> Commit, write a descriptive changelog and select any newly added files.  
CLI: ```svn add *filename*``` any newly added files, then ```svn commit -m "Your Changelog Message"``` or ```svn ci```  
  
-- To see whats going on: --  
TortoiseSVN: File icons change depending on their status, Rightclick -> Show Log and Rightclick -> Check for Modifications are interesting  
CLI: ```svn log``` and ```svn diff``` are interesting
