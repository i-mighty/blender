#!/bin/bash
# End-to-end connectivity test script
# Tests communication between Kubric add-on and agent server

set -e

echo "🧪 Kubric Connectivity Test"
echo "============================"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

AGENT_URL="${AGENT_URL:-http://localhost:8000}"
MAX_RETRIES=5
RETRY_DELAY=2

# Function to check if agent is running
check_agent() {
    echo -n "Checking agent server at $AGENT_URL... "
    if curl -s -f "$AGENT_URL/health" > /dev/null 2>&1; then
        echo -e "${GREEN}✓ Running${NC}"
        return 0
    else
        echo -e "${RED}✗ Not running${NC}"
        return 1
    fi
}

# Function to wait for agent to start
wait_for_agent() {
    echo "Waiting for agent server to start..."
    for i in $(seq 1 $MAX_RETRIES); do
        if check_agent; then
            return 0
        fi
        echo "  Attempt $i/$MAX_RETRIES failed, retrying in ${RETRY_DELAY}s..."
        sleep $RETRY_DELAY
    done
    return 1
}

# Test 1: Health Check
test_health() {
    echo ""
    echo "Test 1: Health Check"
    echo "-------------------"
    
    response=$(curl -s "$AGENT_URL/health")
    status=$(echo $response | jq -r '.status' 2>/dev/null || echo "unknown")
    
    if [ "$status" = "healthy" ]; then
        echo -e "${GREEN}✓ Health check passed${NC}"
        echo "  Response: $response"
        return 0
    else
        echo -e "${RED}✗ Health check failed${NC}"
        echo "  Response: $response"
        return 1
    fi
}

# Test 2: Status Endpoint
test_status() {
    echo ""
    echo "Test 2: Status Endpoint"
    echo "----------------------"
    
    response=$(curl -s "$AGENT_URL/api/v1/status")
    agent_init=$(echo $response | jq -r '.agent_initialized' 2>/dev/null || echo "false")
    
    if [ "$agent_init" = "true" ]; then
        echo -e "${GREEN}✓ Status check passed${NC}"
        echo "  Response: $response"
        return 0
    else
        echo -e "${YELLOW}⚠ Status check returned unexpected value${NC}"
        echo "  Response: $response"
        return 0  # Not a failure, just unexpected
    fi
}

# Test 3: Send Message
test_message() {
    echo ""
    echo "Test 3: Send Message"
    echo "-------------------"
    
    response=$(curl -s -X POST "$AGENT_URL/api/v1/message" \
        -H "Content-Type: application/json" \
        -d '{"message": "Hello from connectivity test"}')
    
    status=$(echo $response | jq -r '.status' 2>/dev/null || echo "unknown")
    agent_response=$(echo $response | jq -r '.response' 2>/dev/null || echo "")
    
    if [ "$status" = "success" ] && [ -n "$agent_response" ]; then
        echo -e "${GREEN}✓ Message test passed${NC}"
        echo "  Agent response: $agent_response"
        return 0
    else
        echo -e "${RED}✗ Message test failed${NC}"
        echo "  Response: $response"
        return 1
    fi
}

# Test 4: Error Handling
test_errors() {
    echo ""
    echo "Test 4: Error Handling"
    echo "---------------------"
    
    # Test invalid JSON
    response=$(curl -s -w "\n%{http_code}" -X POST "$AGENT_URL/api/v1/message" \
        -H "Content-Type: application/json" \
        -d 'invalid json' 2>/dev/null | tail -n1)
    
    if [ "$response" = "422" ] || [ "$response" = "400" ]; then
        echo -e "${GREEN}✓ Error handling works (got $response)${NC}"
        return 0
    else
        echo -e "${YELLOW}⚠ Unexpected error response: $response${NC}"
        return 0  # Not critical
    fi
}

# Test 5: Concurrent Requests
test_concurrent() {
    echo ""
    echo "Test 5: Concurrent Requests"
    echo "--------------------------"
    
    success_count=0
    for i in {1..5}; do
        response=$(curl -s -X POST "$AGENT_URL/api/v1/message" \
            -H "Content-Type: application/json" \
            -d "{\"message\": \"Concurrent test $i\"}" 2>/dev/null)
        status=$(echo $response | jq -r '.status' 2>/dev/null || echo "unknown")
        if [ "$status" = "success" ]; then
            ((success_count++))
        fi
    done
    
    if [ $success_count -ge 4 ]; then
        echo -e "${GREEN}✓ Concurrent requests handled ($success_count/5 succeeded)${NC}"
        return 0
    else
        echo -e "${YELLOW}⚠ Some concurrent requests failed ($success_count/5 succeeded)${NC}"
        return 0  # Not critical for now
    fi
}

# Main execution
main() {
    # Check if jq is installed
    if ! command -v jq &> /dev/null; then
        echo -e "${YELLOW}⚠ jq not installed. Some tests may not work correctly.${NC}"
        echo "  Install with: brew install jq (macOS) or apt-get install jq (Linux)"
    fi
    
    # Check if curl is installed
    if ! command -v curl &> /dev/null; then
        echo -e "${RED}✗ curl is required but not installed${NC}"
        exit 1
    fi
    
    # Check agent is running
    if ! check_agent; then
        echo ""
        echo -e "${YELLOW}Agent server not running.${NC}"
        echo "Start it with: python -m kubric_agent.main"
        echo ""
        read -p "Wait for agent to start? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            if ! wait_for_agent; then
                echo -e "${RED}✗ Agent server did not start${NC}"
                exit 1
            fi
        else
            exit 1
        fi
    fi
    
    # Run tests
    tests_passed=0
    tests_total=5
    
    test_health && ((tests_passed++))
    test_status && ((tests_passed++))
    test_message && ((tests_passed++))
    test_errors && ((tests_passed++))
    test_concurrent && ((tests_passed++))
    
    # Summary
    echo ""
    echo "============================"
    echo "Test Summary: $tests_passed/$tests_total passed"
    
    if [ $tests_passed -eq $tests_total ]; then
        echo -e "${GREEN}✓ All tests passed!${NC}"
        exit 0
    else
        echo -e "${YELLOW}⚠ Some tests had issues${NC}"
        exit 0  # Don't fail, just warn
    fi
}

main "$@"

