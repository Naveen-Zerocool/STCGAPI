##### **Parcel Service Backend API (STCGAPI -> Scalable Tracking Number Generator API)**

**Prerequisites**
1. Docker
2. docker-compose

**Available APIs**
1. api-auth (For session based browsable APIs alone - for testing)
   1. Login
   2. Logout
2. login (For Token based auth - returns a token if valid)
3. api
   1. List parcels created with tracking number and other details
   2. Delete a parcel tracking based on tracking id
   3. Generate a random tracking ID given all mandatory data

**Contains**
1. APIs
2. UI - Frontend with Vue (added login, logout, create based on form, list and delete tracking IDs)
3. Admin site - Add, Update and Delete Users who can login with Session/ Token based auth
4. Browsable APIs

**Admin Site:** 

1. deployed: https://stcgapi-web.onrender.com/admin/
2. local: http://127.0.0.1:8000/admin/

**UI:**

1. deployed: https://stcgapi-web.onrender.com/parcel/
1. local: http://127.0.0.1:8000/parcel/

**Browsable APIs**

1. deployed:
   1. https://stcgapi-web.onrender.com/api/parcels/list/
   2. https://stcgapi-web.onrender.com/api/parcels/<TRACKING-ID>/
   3. https://stcgapi-web.onrender.com/api/next-tracking-number/
   4. https://stcgapi-web.onrender.com/api/next-tracking-number/?origin_country_id=IN&destination_country_id=US&weight=1.0&order_created_at=2024-10-10T19:29:32%2B08:00&customer_id=de619854-b59b-425e-9db4-943979e1bd49&customer_name=GlobalLogistics&customer_slug=global-logistics
2. local:
   1. http://127.0.0.1:8000/api/parcels/list/
   2. http://127.0.0.1:8000/api/parcels/<TRACKING-ID>/
   3. http://127.0.0.1:8000/api/next-tracking-number/
   4. http://127.0.0.1:8000/api/next-tracking-number/?origin_country_id=IN&destination_country_id=US&weight=1.0&order_created_at=2024-10-10T19:29:32%2B08:00&customer_id=de619854-b59b-425e-9db4-943979e1bd49&customer_name=GlobalLogistics&customer_slug=global-logistics

**Steps to Run on Local Machine:**

1. git clone <repo_url>
2. copy .env.example to .env and update the values
3. docker-compose -f docker-compose.yml up -d --build
4. docker exec -it stcgapi-web bash
5. python3 manage.py createsuperuser
6. Navigate to UI URL or browsable API URL to access the application

**Points to Note**

1. Added validations for all input fields
2. Used redis for making the tracking id generation faster and scalable
