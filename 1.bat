@echo off

mkdir frontend
cd frontend

mkdir public

mkdir src
cd src

mkdir components
cd components
type nul > Header.vue
type nul > Footer.vue
type nul > CDKeyExtract.vue
type nul > CDKeyQuery.vue
type nul > UserInfo.vue
cd ..

mkdir views
cd views
type nul > Home.vue
type nul > Login.vue
cd ..

mkdir router
cd router
type nul > index.js
cd ..

mkdir store
cd store
type nul > index.js
cd ..

type nul > App.vue
type nul > main.js
cd ..

type nul > package.json

echo Frontend project structure created successfully!
pause