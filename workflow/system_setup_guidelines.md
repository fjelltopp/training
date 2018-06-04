I am setting up the system on an ec2 instance. I write every steps on this thread.

## Guidelines
### Installation

1. On Amazon AWS create an instance `small.t2` with 20GB of storage. Add http and https ports and enable public IP.
2. Save a key for your instance and run `sudo chmod 400 *.pem` to make it executable
3. `ssh -i who_guidelines_training.pem ubuntu@35.157.141.164` (or whatever is your key an your ip)
4. Fix problem with languages not set on EC2 instance:
Install editor and open the file: 
```
sudo apt-get install mc
mcedit  ~/.bashrc
```
At the end of the file add the following two lines:
```
export LC_ALL="en_US.UTF-8"
export LC_CTYPE="en_US.UTF-8"
```
Then **exit** and log in again to your server!

5. Install packages needed by the installation script:
```
sudo apt-get update
sudo apt-get install python python-pip docker-compose docker
pip install passlib
```
6. Generate a ssh key on the machine. 
```
ssh-keygen
cat ~/.ssh/id_rsa.pub
```
copy this ssh key to the github (https://github.com/settings/keys)

4. Clone all the source code to the new directory:
```
mkdir ~/iees_meerkat
cd ~/iees_meerkat
git clone git@github.com:meerkat-code/meerkat_dev.git
ls ~/iees_meerkat
```
5. Run the setup script which will set up docker containers based with different modules:
```
cd ~/iees_meerkat/meerkat_dev
./mk setup
```

6. Run the system!
```
sudo ./mk up
```
7. The Frontend static assets need to be compiled:
```
sudo ./mk exec frontend setup_static
```
8. To stop `sudo ./mk stop`


### Using tmux and other fancy tools
```
sudo apt-get install tmux htop mc
```
**tmux**
- `Ctrl-b d` - detach
- `tmux attach` - attach to a previous session
- `Ctrl-b %` - split panes horizontally
- `Ctrl-b "` - split panes vertically
- `Ctrl-b UP/DOWN/RIGHT/LEFT` - navigate between panes
{tmux,ctrl-B then D to detach, tmux atach}
- type `exit` in a pane to close the session

**htop**
- `F2` - sort processes
- `F4` - to filter by name (`Enter` to finish`
- `F9` to kill! signal 9 and 15.


### Running Madagascar & Updating inventory
1. Clone private Madagascar config repository:
```
cd ~/iees_meerkat/
git clone git@github.com:meerkat-code/meerkat_mad.git
```
2. Run the website again (you might need to turn it off first: `sudo ./mk stop`). `-f` flag means that we will use automatically generated fake data:
`sudo ./mk up mad -f`
(or `export INITIAL_DATA_SOURCE=FAKE_DATA && export STREAM_DATA_SOURCE=NO_STREAMING && docker-compose -f mad.yml up ` in `meerkat_dev/compose`)

3. Update javascript files by running `gulp` *inside* frontend container:
```
cd ~/iees_meerkat/meerkat_dev/compose
sudo docker exec -ti compose_frontend_1 bash
gulp clean && gulp
```

4. Check the clinics list in the current system: `[ip]/api/locations`
5. Access inventory (https://docs.google.com/spreadsheets/d/1hjCyrZ5RB6VV0DlbTt8CSNzAHWvx42zLT_h0EHOpiuk/edit?usp=sharing_eip&ts=5b0cf131) and download it as a csv file.

6. Normally the file is already edited. You can make your own copy (File-> Save a copy) and do some edits in **your own version**. Then download it.

7. Update the csv file to the server using winscp or `scp -i Training.pem new_inventory.csv ubuntu@[ip]:~/`

8. Use command `file` to compare type of the file of your new inventory and the one in the system (`~/iees_meerkat/meerkat_mad/abacus/locations/mad.clinics.csv`). Use command `dos2unix` or `unix2dos` to make the new inventory the same type as mad_clinics.csv.

9. Overwrite mad_clinics.csv with your new inventory. run `git status` and `git diff` to see your changes.

10. Create a new branch to save your changes to:
```
git checkout -b testinventoryupdate[YOUR_NAME]
git add .
git commit -m "Trying to update the inventory"
```
11. Now stop and start the website to see if your new inventory works on your server. Check the clinics list in the system: `[ip]/api/locations` to cofnirm your changes took place.

12. **If** everything works correctly `git push` your branch to the server, and in Github create a PR (pull request). Well done! (this is just for test, so don't worry we won't accept those changes to the live system :) )

### Adding a new form to demo site

An example of changes needed to add parts of the simple form (https://github.com/meerkat-code/madagascar_feedback/issues/118) are here:
https://github.com/meerkat-code/meerkat_mad/compare/malaria_tab...new_form_exercise

And in text:
```
diff --git a/abacus/data_types.csv b/abacus/data_types.csv
index 727e0cc..537f038 100644
--- a/abacus/data_types.csv
+++ b/abacus/data_types.csv
@@ -1,5 +1,6 @@
 name,type,form,db_column,condition,date,var,uuid,location,multiple_row
 Case Report,case,mad_case,,,pt./visit_date,tot_1,meta/instanceID,deviceid,
+Sentinel,case,mad_sentinel,,,clinic./date_envoi,sent_1,meta/instanceID,deviceid,
 Register,register,mad_register,,,intro./visit_date,reg_1,meta/instanceID,deviceid,
 Outbreak Investigation,case,mad_plague,,,today,tot_1,meta/instanceID,"in_geometry$gps/Longitude,gps/Latitude","pt$./age$,pt$./gender$,pt$./occupation$,cd$./status$,plague_rdt$,plague_type$"
 Stock Level Notification,register,mad_stock,,,SubmissionDate,stock_1,meta/instanceID,deviceid,
diff --git a/abacus/mad_config.py b/abacus/mad_config.py
index 2aea216..65605a0 100755
--- a/abacus/mad_config.py
+++ b/abacus/mad_config.py
@@ -12,7 +12,8 @@ country_config = {
         "mad_district_stock",
         "mad_plague",
         "mad_stock",
-        "mad_contacts"
+        "mad_contacts",
+        "mad_sentinel"
  #       "mad_ipm"
     ],
     "tables_uuid": {
@@ -23,6 +24,7 @@ country_config = {
         "mad_plague": "meta/instanceID",
         "mad_stock":"meta/instanceID",
         "mad_contacts":"meta/instanceID",
+        "mad_sentinel":"meta/instanceID",
         "mad_ipm": "uuid"
 
     },
@@ -334,6 +336,12 @@ country_config = {
             "J_7/signes_infectieux": {"multiple":[ "firevre","cephalees","frisson","courbure","asthenie" ]},
             "J_7/statut_actuel": {"one":["actif","non_actif"]},
             "J_7/statut_finale": {"one":[ "pas_malade","perdu_de_vue","suspect_et_transfere_fs","suspect_et_evade","decede","redevenu_contact" ]}
+        },
+        "mad_sentinel":{
+            "clinic./date_envoi":{"date":"year"},
+            "clinic./nature_prelevement":{"one":["gorge","naso","bubon","lcr"]},
+            "opinion./genre":{"one":["m","f"]},
+            "information./age":{"integer":[0,120]}
         }
     },
     "alert_data": {
diff --git a/abacus/variable_codes/mad_codes.csv b/abacus/variable_codes/mad_codes.csv
index 0890e5c..bee3d98 100644
--- a/abacus/variable_codes/mad_codes.csv
+++ b/abacus/variable_codes/mad_codes.csv
@@ -1,10 +1,13 @@
 id,name,type,form,multiple_link,db_column,alert,alert_type,method,condition,category,calculation,calculation_group,calculation_priority,disregard,classification_casedef,source,source_link,alert_desc,case_def,case_def::french,risk_factors,risk_factors::french,symptoms,symptoms::french,labs_diagnostics,labs_diagnostics::french,questions::french,
 submission_date,Submission Date,case,mad_case,,SubmissionDate,,,value,,,,,,,,,,,,,,,,,,,,
 tot_1,Total,case,mad_case,,SubmissionDate,,,not_null,,key_indicators,,,,,,,,,,,,,,,,,,
+sent_1,Total Sentinel,case,mad_sentinel,,SubmissionDate,,,not_null,,key_indicators,,,,,,,,,,,,,,,,,,
 cv_1,Total contact visits,visit,mad_contacts,,SubmissionDate,,,not_null,,key_indicators,,,,,,,,,,,,,,,,,,
 con_1,Total contacts,case,mad_contacts,,SubmissionDate,,,not_null,,key_indicators,,,,,,,,,,,,,,,,,,
 gen_1,Male,case,mad_case,,pt./gender,,,match,male,gender,,gender,,,,,,,,,,,,,,,,
 gen_2,Female,case,mad_case,,pt./gender,,,match,female,gender,,gender,,,,,,,,,,,,,,,,
+sent_gen_1,Male,case,mad_sentinel,,opinion./genre,,,match,m,gender,,gender,,,,,,,,,,,,,,,,
+sent_gen_2,Female,case,mad_sentinel,,opinion./genre,,,match,f,gender,,gender,,,,,,,,,,,,,,,,
 nat_1,Madagascar,case,mad_case,,nationality,,,match,madagascar,nationality,,nationality,,,,,,,,,,,,,,,,
 nat_2,Kenya,case,mad_case,,nationality,,,match,kenya,nationality,,nationality,,,,,,,,,,,,,,,,
 nat_3,Other Nationality,case,mad_case,,nationality,,,match,other,nationality,,nationality,,,,,,,,,,,,,,,,
```

# Loading new test data from a csv.
Add a new form definitions to the system like in the previous example.
Copy csv file containing submissions to 
`iees_meerkat/meerkat_abacus/meerkat_abacus/data`
This directory contains csv dump of all data previously loaded in the system so if you used fake data (`-f`) before it will contain generated csv for other forms.

Then start system in `meerkat_dev/compose` (!)
`export INITIAL_DATA_SOURCE=LOCAL_CSV && export STREAM_DATA_SOURCE=NO_STREAMING && docker-compose -f mad.yml up`



