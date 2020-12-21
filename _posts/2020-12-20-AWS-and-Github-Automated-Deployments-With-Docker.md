# Automated Deployments With Github Actions, Docker and AWS

# Requirements

---

- NodeJS (https://nodejs.org) - If you decide to follow-along

# Generate A Sample Application To Deploy

---

We are going to be auto-generating a "dummy" application to represent what we want to host. For this use-case, we will be using `create-react-app`. This is *not* required, as is simply just a simple use-case for generating a dummy application with unit tests. Feel free to use something like Java, Ruby, etc. If that is your language of choice. 

In your **Terminal**, execute the following commands. 

```bash
$ npx create-react-app my-sample-application
```

# Creating A Dockerfile For Development

---

It's good practice to separate development and production Docker. This will allow you to easily iterate locally within a Docker-based environment. When you want to go prod, the pipeline will reference the production-based Dockerfile. 

**Dockerfile.development**

```docker
FROM node:alpine

WORKDIR '/app'

COPY package.json .
RUN npm install

COPY . .

CMD ["npm", "run", "start"]
```

**docker-compose-dev.yml**

```docker
version: '3'
services:
  web:
    stdin_open: true
    build:
      context: .
      dockerfile: Dockerfile.development
    ports:
      - '3000:3000'
    volumes:
      - /app/node_modules
      - .:/app
```

Now, whenever we want to run our development environment, we can simply execute the following:

`docker-compose -f docker-compose-dev.yml up`

Because we mounted the files into the container from our host machine, any changes done locally will automatically be reflected in the container.  This is useful for quick development. 

# Creating A Dockerfile For Production

---

Production environments typically have a different setup than dev. We want *minified* assets and want to remove some of the bloat we'd get with the standard development server. 

1. Add the commands to get the static assets from building the static files
2. Use Nginx to host these static assets from within the container

**Dockerfile**

```docker
FROM node:alpine
WORKDIR '/app'
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx
COPY --from=0 /app/build /usr/share/nginx/html
```

**docker-compose.yml**

```docker
version: '3'
services:
  web:
    stdin_open: true
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - '80:80'
```

# Generating An Elastic Beanstalk Application & Environment

---

Elastic Beanstalk is a fantastic orchestration service offered by AWS used for deploying applications into AWS. Beanstalk will easily handle elastic load balancers and auto-scaling for you and can also reference docker files to spin up applications automatically. This is what we'll do in this section. 

### Create An Environment

In AWS, search for "Elastic Beanstalk" and open it up

![Automated%20Deployments%20With%20Github%20Actions,%20Docker%20%20c50106dfb7734b00b888a43c0ced094a/Untitled.png](Automated%20Deployments%20With%20Github%20Actions,%20Docker%20%20c50106dfb7734b00b888a43c0ced094a/Untitled.png)

From here, we'll create a new application.  Select "Create New Environment"

![Automated%20Deployments%20With%20Github%20Actions,%20Docker%20%20c50106dfb7734b00b888a43c0ced094a/Untitled%201.png](Automated%20Deployments%20With%20Github%20Actions,%20Docker%20%20c50106dfb7734b00b888a43c0ced094a/Untitled%201.png)

Type in the application name, environment, etc. If you're using Node.JS, ensure the platform is NodeJS and if Java, select Java, etc. 

This process will take 5-10 minutes to complete fully once you select Create Environment. 

# Connecting GitHub to AWS

---

We want to ensure the flow from Github merge → AWS is automated. That is, once we merge new code into the main branch, how can we automate the new code deployments to our cloud server? 

1. Add secrets into your GitHub account 
    1. The secrets will match the access key and secret when creating a new IAM user

### Creating A New GitHub Action

```yaml
name: Test & Deploy
on:
  push:
    branches:
      - master
jobs:
  test-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Latest Repo
        uses: actions/checkout@master

      # Zip Dockerfile for upload
      - name: Generate Deployment Package
        run: zip -r deploy.zip * -x "**node_modules**"
        
      - name: Get timestamp
        uses: gerred/actions/current-time@master
        id: current-time

      - name: Run string replace
        uses: frabert/replace-string-action@master
        id: format-time
        with:
          pattern: '[:\.]+'
          string: "${{ steps.current-time.outputs.time }}"
          replace-with: '-'
          flags: 'g'

      - name: Deploy to EB
        uses: einaregilsson/beanstalk-deploy@v14
        with:
          aws_access_key: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws_secret_key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          application_name: beanstalk-engineer-v2
          environment_name: BeanstalkEngineerV2-env
          version_label: "the-simple-engineer-deployment-${{ steps.format-time.outputs.replaced }}"
          region: us-east-2
          deployment_package: deploy.zip
```

The above wil generate a zip file from the contents (except for node_modules) and this is what will be uploaded into S3 under the EB environment. EB for single container deployments will scan for the docker-compose file and build the image for you and deploy. 

I use timestamp and string replace commands to get a unique suffix for the zip file I upload into S3. The S3 upload is automated in EB. 

Once you make a new commit to master, the code will be deployed and you'll be able to access your site on the Elastic Beanstock URL seen on the AWS EB service page. 

![Automated%20Deployments%20With%20Github%20Actions,%20Docker%20%20c50106dfb7734b00b888a43c0ced094a/Untitled%202.png](Automated%20Deployments%20With%20Github%20Actions,%20Docker%20%20c50106dfb7734b00b888a43c0ced094a/Untitled%202.png)