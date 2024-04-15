Current Code version: v.1.0.2

First time cloneing repo - create gitignore if it does not exist
ctrl+shift+p
Add gitignore

simulate cms testing

legacy php code example - main controller


                let itemProperties = {"Title":input_title,"FullName":idName,"Address":idAddress, "City":idCity, "State":idState, "Zip":idZip,
                    "Email":idEmail,"Phone":idPhone,"Make":idMake,"Model":idModel
                    ,"Year": idYear ,"PurchaseDate": idPurchased, "Part":idPart, "Subject":idSubject, "Description":idDescription
                    ,"Link1":
                        {"__metadata": { "type": "SP.FieldUrlValue" },
                            "Description": "Link1",
                            "Url": link1
                        }
                    ,"Link2":
                        {"__metadata": { "type": "SP.FieldUrlValue" },
                            "Description": "Link2",
                            "Url": link2
                        }

                    ,"__metadata":{"type":"SP.Data.NightVisionListItem"}
                };

---

 if(this.byId("idImageReceiptHidden").getValue() !==null && this.byId("idImageReceiptHidden").getValue() !== ""){
                var img1 = app_url +  savedImageDirectory + "/" + this.byId("idImageReceiptHidden").getValue();
            }
            if(this.byId("idImagePartHidden").getValue() !==null && this.byId("idImagePartHidden").getValue() !== ""){
                var img2 = app_url +  savedImageDirectory + "/" + this.byId("idImagePartHidden").getValue();
            }

--- local vsc run and debug
file:///C:/Users/bsteiner/OneDrive%20-%20Old%20World%20Industries/Documents/Git%20Repos/sharepoint_api_b2c_tester_webpage/sharepoint_api_test.html            

-- local vsc with launch.json config
{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        {
            "type": "chrome",
            "request": "launch",
            "name": "Open sharepoint_api_test.html",
            "file": "c:\\Users\\bsteiner\\OneDrive - Old World Industries\\Documents\\Git Repos\\sharepoint_api_b2c_tester_webpage\\sharepoint_api_test.html"
        }
    ]
}

========================================================================================
============================== CF app: sharepoint_api_b2c ==============================
==== TEST EXAMPLES

== LOCAL BAS
https://port9009-workspaces-ws-wnjc7.us10.applicationstudio.cloud.sap/getUsers/Warranty

== CF QA - OWITEST
https://owitest-dev-sharepoint-api-nodejsserver.cfapps.us10.hana.ondemand.com/getTitle/Warranty

== CF PROD - OWI
https://owi-production-sharepoint-api-nodejsserver.cfapps.us10.hana.ondemand.com/getTitle/Warranty

------- FROM cf app READ.ME

-- testing - first start node server.js
cd sharepoint_api_nodeJsServer/
node server.js
-- bottom left should now have a popup to click on to start a browser session ie:
     https://workspaces-ws-wnjc7-app2.us10.applicationstudio.cloud.sap/
-- now leave that terminal open (live) and start a new terminal for running commands
-- note: your server console.log messages will now appear in your first terminal session where node was started

-- testing from browser page
1) go to dir with server.js    -- and run below  --- same as above
2) node server.js - that will expose external url    ====== or click debug icon to run and debug
3) example: https://port9009-workspaces-ws-wnjc7.us10.applicationstudio.cloud.sap/getTitle/Warranty
            https://port9009-workspaces-ws-wnjc7.us10.applicationstudio.cloud.sap/getUsers/Warranty

-- Testing using curl
1) run debug - attach         ---- this is optional -- not necessary --------------  make sure you have server.js tab open when running icon
2) from terminal: curl --request GET  --url http://localhost:9009/getTitle/Warranty

 
    test example: https://port9009-workspaces-ws-wnjc7.us10.applicationstudio.cloud.sap/getUsers/Warranty
    site examples:
        https://oldworld.sharepoint.com/sites/Warranty/_api/web/siteusers
        https://oldworld.sharepoint.com/sites/Warranty/_api/web/siteusers?$select=Id,Title,LoginName,Email
		 
	// Get List Items by List Name.   	// https://oldworld.sharepoint.com/sites/Warranty/_api/web/lists/getbytitle('NightVisionWarranty')/items	
	// https://oldworld.sharepoint.com/sites/Warranty/_api/web/lists/getbytitle('NightVisionWarranty')/items?$select=&$filter=&$orderby=Created%20desc 


// Issues debuging BAS nodeJs service using this html app.

// Result: deploy to CF QA and open the CF log to debug any issues - note may have to add server.js code for additional logging

for QA got to owitest, dev space, app sharepoint_api_nodeJsServer
on left menu click logs
then call the url: https://owitest-dev-sharepoint-api-nodejsserver.cfapps.us10.hana.ondemand.com/getTitle/Warranty
and watch the new messages logged (click refresh)

==================== GIT Examples ====================
example 1. develop-bill changes locally
first pull develop branch to create your local branch in the image of:
first time create local branch example:  git checkout -b develop-bill

====================
-- example to merge develop-bill into develop and merge develop into master and create a version tag
-- develop-local
git status # make sure you see the changed files you expect to see
git add -A
git commit -m "added readme notes for git examples
git push

-- develop 
git checkout develop && git pull 
git merge develop-bill
git push

-- master
git checkout master && git pull
git merge develop
git push

-- tag it
git tag -a task_id_v1.0.1 -m "Releasing version v1.0.1"
git push origin --tags

-- reload your personal branch so not to accidentially hammer master branch
git checkout develop-bill && git pull 

====================