#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from supabase import create_client


SUPABASE_URL = "https://fcibqtbavrltcvzhfgjy.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZjaWJxdGJhdnJsdGN2emhmZ2p5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Njk0MDIwNjMsImV4cCI6MjA4NDk3ODA2M30.dZCE7TpUZWHnT3vUvuviAZqfi9_MFwqkQHBk0RZNb9A"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

