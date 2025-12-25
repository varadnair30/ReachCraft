"""
Supabase client initialization
"""
from supabase import create_client, Client
import os
from functools import lru_cache


@lru_cache()
def get_supabase_client() -> Client:
    """
    Get Supabase client instance (singleton pattern)
    Uses environment variables:
    - SUPABASE_URL
    - SUPABASE_KEY
    """
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")

    if not supabase_url or not supabase_key:
        raise ValueError(
            "Missing Supabase credentials. "
            "Please set SUPABASE_URL and SUPABASE_KEY in your .env file"
        )

    return create_client(supabase_url, supabase_key)