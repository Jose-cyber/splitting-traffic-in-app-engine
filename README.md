# Splitting traffic in app-engine

<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/googlecloud/googlecloud-original-wordmark.svg"/>

In this project I will show you how to split traffic in app engine, where you can specify a porcentage distribution of traffic across two or more of the versions of your application.

## Required:
  - Google Cloud Account.
  - gcloud CLI installed.


## What is app-engine ?
**App Engine is a fully managed, serverless platform for developing and hosting web applications at scale**. You can choose from several popular languages, libraries, and frameworks to develop your apps, and then **let App Engine take care of provisioning servers and scaling your app instances based on demand.**

## Create a project and enable required clud apis.

After being authenticated in gcloud command run these commands bellow to create a project and enable required apis, if you don't know how to being authenticated [click here](https://cloud.google.com/docs/authentication/gcloud), or you can use [cloud shell](https://cloud.google.com/shell/docs/launching-cloud-shell) to run theese commands.


Let's create a project, in this example I'm calling my project of **split-traffic**, you also can set the name of your project in a varible called ```PROJECT_ID``` runing a export command in your shell/bash:<br>
<pre>
export PROJECT_ID=split-traffic
</pre>

Create a project:
<pre>
gcloud projects create $PROJECT_ID
</pre>

Set project in your shell:
<pre>
gcloud config set project $PROJECT_ID
</pre>

Enable app-engine api:
<pre>
gcloud services enable appengine.googleapis.com --project $PROJECT_ID
</pre>


After you run these commands, you'll can see in your project the initial page of App Engine:

![](./img/app-engine-1.png)


## Deploy web application

In app engine we've a 2 kind of environments, they're standard and flexible, in this example we will deploy the app using the standard environment, if you want  to know more about the difference of theese environments [click here](https://cloud.google.com/appengine/docs/the-appengine-environments).

Access the app directory:
<pre>
cd app/
</pre>

Deploying app:
<pre>
gcloud app deploy app.yaml --project $PROJECT_ID
</pre>
this is an example of the command output:
![](./img/app-engine-deploy.png)


After you deploy the app, the app engine will generate a Default URL following the template below:

https://**VERSION**-dot-**SERVICE**-dot-**PROJECT_ID**.**REGION_ID**.r.appspot.com


 - **VERSION**: is the name of your version, and the version name can contain numbers, letters, and hyphens, you also can omit "**VERSION**-dot-" if you don't need to target a specific version, in this project I'm not setting any version name on my configuration file([app/app.yaml](app/app.yaml)). 
 - **SERVICE**: is the app name, in this case ```python-app```.
 - **PROJECT_ID**: is the project id where's you activated the app engine resource and deployed the app, I've created a project with PROJECT_ID called ```split-traffic```.
 - **REGION_ID**:  The app engine is a region resource, in this case chose the ```us-central```.

In this case I will access the app using this url:

https://python-app-dot-split-traffic.uc.r.appspot.com

![](./img/app-engine-browser.png)

## App engine components

It's really important we know the app engine components, to understand about how we can split traffic in this resource. 

<img src="https://cloud.google.com/static/appengine/docs/images/modules_hierarchy.svg"/>

The App Engine **application** is a top-level container that includes the **service**, **version**, and **instance** resources that make up your app.

when we deploy the python app using the command "gcloud app deploy ....[]" a **service** called "python-app" was instantly created and **the service in the app engine can have one or more versions**, you can list the versions using the command:
<pre>
gcloud app versions list --service=python-app --project $PROJECT_ID
</pre>
output:
<img src="img/app-engine-versions.png"/>

The **versions** run on the **instances**, and what I'm going to do is create a new version of "python-app" service and with this second version deployed, we can split the traffic so that only a percentage of accesses view the new version

In the next steps below, I'll show you how to deploy a new version of our python app, and split traffic between these versions. 

## Deploy the new version

To create a new version of our app, let's start edditing our [main.py](app/main.py) file, and change the message string that was being returned in the ```index()``` function, from "App 1" to "App 2".

<img src="img/code_change.png"/>

After making the change and saving it, let's deploy the new version of service python-app, this version I'll call it of "potato-version" .

Acess de app directory:
<pre>
cd app/
</pre>

Deploy the new version:
<pre>
gcloud app deploy app.yaml --project $PROJECT_ID --version potato-version --no-promote
</pre>
output:
<img src="img/deployed-new-version.png"/>
In the command used to deploy the new version, 2 very important arguments were used, which are:
 
  - --version: where we set the name of version.
  - --no-promote: this command is to version of we're deploying do not receive all traffic:

Now we can list the versions and see the potato-version deployed.
<pre>
gcloud app versions list --service=python-app --project $PROJECT_ID
</pre>
output:
<img src="img/list-versions.png">

## Splitting traffic between the services

You can use traffic splitting to specify a percentage distribution of traffic across two or more of the versions within a service. Splitting traffic allows you to conduct A/B testing between your versions and provides control over the pace when rolling out features.

Sintax:
<pre>
gcloud app services set-traffic [MY_SERVICE] --splits [MY_VERSION1]=[VERSION1_WEIGHT],[MY_VERSION2]=[VERSION2_WEIGHT] --split-by [IP_OR_COOKIE_OR_RANDOM]
</pre>

split traffic:
<pre>
gcloud app services set-traffic python-app --splits 20240117t144713=0.5,potato-version=0.5 --split-by random --project $PROJECT_ID
</pre>

run the script.sh using the command:
<pre>
./script.sh your-app-host.appspot.com
</pre>
and the output we can see the traffic beeing the thr between the diference versions
<img src="img/split-traffic-working.png"/>

## Migrate traffic

Let's migrate all traffic to our newest version, and turn off the traffic for old version

sintax:
<pre>
gcloud app services set-traffic [MY_SERVICE] --splits [MY_VERSION]=1
</pre>
executing this command you will migrate all traffic immediately, but if you want migrate gradually, add the flag ```--migrate``` in command.

Command:
<pre>
gcloud app services set-traffic python-app --splits potato-version=1 --project $PROJECT_ID
</pre>
output:
<img src="img/migrate-traffic.png">

now you can see, that all traffic is only in one version:
<img src="img/all-traffic-in-one-version.png">





























































































