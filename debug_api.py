#!/usr/bin/env python3
"""
Debug script for Jokes API connection
"""
import asyncio
import logging
import requests
import json
from config import Config

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_api_connection():
    """Test API connection and diagnose issues"""
    print("🔍 Diagnosing Jokes API connection...\n")
    
    # 1. Check configuration
    print("1️⃣ Configuration Check:")
    print(f"   JOKES_API_URL: {Config.JOKES_API_URL}")
    print(f"   JOKES_API_ENDPOINT: {Config.JOKES_API_ENDPOINT}")
    print(f"   Full API URL: {Config.get_jokes_api_url()}")
    print(f"   JOKES_API_TIMEOUT: {Config.JOKES_API_TIMEOUT}")
    print(f"   JOKES_API_KEY: {'SET' if Config.JOKES_API_KEY else 'NOT SET'}")
    print(f"   Headers: {Config.JOKES_API_HEADERS}")
    print()
    
    # 2. Test basic connectivity
    print("2️⃣ Basic Connectivity Test:")
    api_url = Config.get_jokes_api_url()
    if not api_url:
        print("   ❌ ERROR: JOKES_API_URL is not configured!")
        return
    
    try:
        # Test basic HTTP connection
        response = requests.get(api_url.replace('/api/getJoke', ''), timeout=5)
        print(f"   ✅ Base URL accessible: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("   ❌ ERROR: Cannot connect to API server")
        print("   💡 Check if joke-api container is running:")
        print("      docker-compose ps")
        print("      docker-compose logs joke-api")
        return
    except requests.exceptions.Timeout:
        print("   ❌ ERROR: Connection timeout")
        return
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
        return
    
    # 3. Test API endpoint
    print("\n3️⃣ API Endpoint Test:")
    try:
        request_data = {"input": "Test joke request"}
        response = requests.post(
            api_url,
            json=request_data,
            timeout=Config.JOKES_API_TIMEOUT,
            headers=Config.JOKES_API_HEADERS
        )
        
        print(f"   Status Code: {response.status_code}")
        print(f"   Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            print("   ✅ API endpoint working correctly!")
            try:
                joke_data = response.json()
                print(f"   Response Data: {json.dumps(joke_data, indent=2)}")
            except json.JSONDecodeError:
                print("   ⚠️  WARNING: Response is not valid JSON")
                print(f"   Raw Response: {response.text}")
        elif response.status_code == 500:
            print("   ❌ ERROR: Internal Server Error (500)")
            print("   💡 Possible causes:")
            print("      - Joke API server is not properly configured")
            print("      - Database connection issues in joke-api")
            print("      - Missing environment variables in joke-api")
            print("      - Joke API code has bugs")
            print(f"   Response: {response.text}")
        elif response.status_code == 404:
            print("   ❌ ERROR: Endpoint not found (404)")
            print("   💡 Check if endpoint path is correct")
        elif response.status_code == 401:
            print("   ❌ ERROR: Unauthorized (401)")
            print("   💡 Check API key configuration")
        elif response.status_code == 403:
            print("   ❌ ERROR: Forbidden (403)")
            print("   💡 Check API permissions")
        else:
            print(f"   ❌ ERROR: Unexpected status code {response.status_code}")
            print(f"   Response: {response.text}")
            
    except requests.exceptions.Timeout:
        print("   ❌ ERROR: Request timeout")
        print("   💡 Try increasing JOKES_API_TIMEOUT")
    except requests.exceptions.ConnectionError:
        print("   ❌ ERROR: Connection failed")
        print("   💡 Check if joke-api container is running and accessible")
    except Exception as e:
        print(f"   ❌ ERROR: {e}")

async def test_docker_containers():
    """Test Docker containers status"""
    print("\n4️⃣ Docker Containers Check:")
    print("   Run these commands to check container status:")
    print("   docker-compose ps")
    print("   docker-compose logs telegram-bot")
    print("   docker-compose logs joke-api")
    print("   docker network ls")
    print("   docker network inspect telegram-bot_bot-network")

async def test_network_connectivity():
    """Test network connectivity between containers"""
    print("\n5️⃣ Network Connectivity Test:")
    print("   To test network connectivity, run:")
    print("   docker exec telegram-bot ping joke-api")
    print("   docker exec telegram-bot curl http://joke-api:8080")
    print("   docker exec joke-api curl http://telegram-bot:8000")

async def main():
    """Run all diagnostic tests"""
    print("🚀 Jokes API Diagnostic Tool\n")
    
    await test_api_connection()
    await test_docker_containers()
    await test_network_connectivity()
    
    print("\n📋 Troubleshooting Steps:")
    print("1. Check if both containers are running: docker-compose ps")
    print("2. Check joke-api logs: docker-compose logs joke-api")
    print("3. Check telegram-bot logs: docker-compose logs telegram-bot")
    print("4. Restart containers: docker-compose restart")
    print("5. Rebuild containers: docker-compose up --build")
    print("6. Check network: docker network inspect telegram-bot_bot-network")
    
    print("\n🎯 Common Solutions:")
    print("- Make sure JokeWebApi is properly built and running")
    print("- Check if joke-api is listening on port 8080")
    print("- Verify network configuration in docker-compose.yml")
    print("- Check if joke-api has proper environment variables")
    print("- Ensure joke-api database/API is properly configured")

if __name__ == "__main__":
    asyncio.run(main())
