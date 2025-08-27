from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime, timedelta
import random
import requests

def fetch_blinkr_data(start_date, end_date):
    """Fetch disbursal data from Blinkr API"""
    if not start_date or not end_date:
        print(f"Missing date parameters: start_date={start_date}, end_date={end_date}")
        return []
    
    # Check if start and end dates are the same
    is_same_date = start_date == end_date
    print(f"Fetching Blinkr API data for dates: {start_date} to {end_date}")
    if is_same_date:
        print(f"⚠️  Same date detected: {start_date} - This should return data for a single day")
    
    # For same dates, try multiple approaches:
    # 1. First try with same start and end date
    # 2. If that fails, try with end date as next day (some APIs expect this)
    # 3. Try with start date as previous day (some APIs expect this)
    api_urls_to_try = []
    
    if is_same_date:
        # Try same date first
        api_urls_to_try.append(f"https://backend.blinkrloan.com/insights/v1/disbursal2?startDate={start_date}&endDate={end_date}")
        
        # Try with end date as next day
        try:
            from datetime import datetime, timedelta
            next_day = (datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d')
            api_urls_to_try.append(f"https://backend.blinkrloan.com/insights/v1/disbursal2?startDate={start_date}&endDate={next_day}")
            print(f"🔄 Will also try alternative URL for same date: startDate={start_date}&endDate={next_day}")
        except Exception as e:
            print(f"Could not calculate next day: {e}")
        
        # Try with start date as previous day
        try:
            from datetime import datetime, timedelta
            prev_day = (datetime.strptime(start_date, '%Y-%m-%d') - timedelta(days=1)).strftime('%Y-%m-%d')
            api_urls_to_try.append(f"https://backend.blinkrloan.com/insights/v1/disbursal2?startDate={prev_day}&endDate={end_date}")
            print(f"🔄 Will also try alternative URL for same date: startDate={prev_day}&endDate={end_date}")
        except Exception as e:
            print(f"Could not calculate previous day: {e}")
    else:
        # Different dates - ensure inclusive range by extending end date by 1 day
        # This ensures we get all data from start_date through end_date (inclusive)
        try:
            from datetime import datetime, timedelta
            end_date_inclusive = (datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d')
            api_urls_to_try.append(f"https://backend.blinkrloan.com/insights/v1/disbursal2?startDate={start_date}&endDate={end_date_inclusive}")
            print(f"📅 Inclusive date range: {start_date} to {end_date} (API call: startDate={start_date}&endDate={end_date_inclusive})")
        except Exception as e:
            print(f"Could not calculate inclusive end date: {e}")
            # Fallback to original dates
            api_urls_to_try.append(f"https://backend.blinkrloan.com/insights/v1/disbursal2?startDate={start_date}&endDate={end_date}")
    
    for i, api_url in enumerate(api_urls_to_try):
        print(f"Trying API URL {i+1}: {api_url}")
        
        try:
            response = requests.get(api_url, timeout=30)
            print(f"Blinkr API response status: {response.status_code}")
            response.raise_for_status()
            data = response.json()
            print(f"Blinkr API response data type: {type(data)}, length: {len(data) if isinstance(data, dict) else 'N/A'}")
            
            # API returns dict with "0","1",.. keys, convert to list
            result = list(data.values())
            print(f"Processed {len(result)} applications from Blinkr API")
            
            if len(result) > 0:
                if is_same_date and i == 1:  # Second URL worked (next day)
                    print(f"✅ Same date data retrieved using alternative URL (next day end date)")
                elif is_same_date and i == 2:  # Third URL worked (previous day)
                    print(f"✅ Same date data retrieved using alternative URL (previous day start date)")
                
                # Debug: Check the structure of the first few applications
                print(f"🔍 Debug: Checking data structure of first few applications")
                for idx, app in enumerate(result[:3]):  # Check first 3 applications
                    print(f"   App {idx + 1} keys: {list(app.keys()) if isinstance(app, dict) else 'Not a dict'}")
                    if isinstance(app, dict):
                        print(f"   App {idx + 1} state: {app.get('state', 'NOT_FOUND')}")
                        print(f"   App {idx + 1} city: {app.get('city', 'NOT_FOUND')}")
                        print(f"   App {idx + 1} tenure: {app.get('tenure', 'NOT_FOUND')}")
                        # Check for alternative field names
                        print(f"   App {idx + 1} state alternatives: {app.get('State', 'NOT_FOUND')} (State), {app.get('state_name', 'NOT_FOUND')} (state_name)")
                        print(f"   App {idx + 1} city alternatives: {app.get('City', 'NOT_FOUND')} (City), {app.get('city_name', 'NOT_FOUND')} (city_name)")
                
                return result
            else:
                print(f"⚠️  URL {i+1} returned 0 results")
                
        except requests.exceptions.RequestException as e:
            print(f"Error with URL {i+1}: {str(e)}")
            continue
    
    if is_same_date:
        print(f"❌ All attempts failed for same date {start_date}")
        print(f"   The Blinkr API might not support same start/end dates or there's no data for {start_date}")
        print(f"   Tried URLs: {api_urls_to_try}")
    
    return []

def login_view(request):
    """Login page view"""
    print("Login view accessed")  # Debug print
    return render(request, 'login.html')

def dashboard_view(request):
    """Dashboard/Disbursal view - requires authentication"""
    print(f"Dashboard view accessed with path: {request.path}")  # Debug print
    print(f"Session data: {dict(request.session)}")  # Debug print
    print(f"Session ID: {request.session.session_key}")  # Debug print
    
    # Simple authentication check (in production, use proper Django auth)
    if request.session.get('authenticated'):
        print("User authenticated, rendering dashboard")  # Debug print
        
        # Create response with cache control headers
        response = render(request, 'dashboard/dashboard.html')
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        
        return response
    else:
        print("User not authenticated, redirecting to login")  # Debug print
        return redirect('/login/')

def authenticate_user(request):
    """Simple authentication endpoint"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        print(f"Authentication attempt - Username: {username}, Password: {password}")
        
        if username == 'Admin' and password == 'Admin@123':
            print("Credentials valid, setting session")
            
            # Force session creation
            if not request.session.session_key:
                request.session.create()
            
            request.session['authenticated'] = True
            request.session.modified = True
            request.session.save()
            
            print(f"Session ID: {request.session.session_key}")
            print(f"Session data after login: {dict(request.session)}")
            
            return redirect('/disbursal/')
        else:
            print("Invalid credentials")
            return render(request, 'login.html', {'error_message': 'Invalid username or password'})
    
    # If not POST, redirect to login
    return redirect('/login/')

def logout_view(request):
    """Logout view - completely clears session and prevents back button access"""
    # Clear all session data
    request.session.flush()
    
    # Create response with cache control headers
    response = redirect('/login/')
    
    # Add headers to prevent caching and back button access
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    
    # Clear any existing cookies
    response.delete_cookie('sessionid')
    
    print("User logged out - session cleared and cache headers set")
    return response

def test_view(request):
    """Test view to verify routing"""
    return JsonResponse({
        'message': 'Test route working', 
        'path': request.path,
        'session_data': dict(request.session),
        'session_key': request.session.session_key,
        'authenticated': request.session.get('authenticated', False)
    })

@csrf_exempt
def summary_data(request):
    """API endpoint for summary data with date filtering"""
    # Check authentication
    if not request.session.get('authenticated'):
        return JsonResponse({"error": "Authentication required"}, status=401)
    
    # Get date parameters
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    # Get filter parameters
    reloan_filter = request.GET.get('reloan', '')
    active_filter = request.GET.get('active', '')
    tenure_filter = request.GET.get('tenure', '')
    state_filter = request.GET.get('state', '')
    city_filter = request.GET.get('city', '')
    
    print(f"Summary data requested - Start: {start_date}, End: {end_date}")
    print(f"Filters: Reloan={reloan_filter}, Active={active_filter}, Tenure={tenure_filter}, State={state_filter}, City={city_filter}")
    
    # Use Blinkr API data instead of mock data
    apps = fetch_blinkr_data(start_date, end_date)
    
    if not apps:
        return JsonResponse({
            "total_applications": 0,
            "total_sanction_amount": 0,
            "total_disbursed_amount": 0,
            "total_pf_amount": 0,
            "total_interest_amount": 0,
            "total_repayment_amount": 0,
            "avg_disbursal": 0
        })
    
    print(f"Processing {len(apps)} applications from Blinkr API")
    
    # Calculate totals from Blinkr API data
    total_sanction_amount = 0
    total_disbursed_amount = 0
    total_pf_amount = 0
    total_interest_amount = 0
    total_repayment_amount = 0
    filtered_applications = 0  # Counter for filtered applications
    
    for app in apps:
        # Apply filters if specified
        if reloan_filter:
            is_reloan_case = app.get('is_reloan_case', False)
            if reloan_filter == 'reloan' and not is_reloan_case:
                continue
            elif reloan_filter == 'new' and is_reloan_case:
                continue
        
        # Apply active filter using is_lead_closed field from API
        if active_filter:
            is_lead_closed = app.get('is_lead_closed', False)
            if active_filter == 'active' and is_lead_closed:
                continue  # Skip closed leads when filtering for active cases
            elif active_filter == 'inactive' and not is_lead_closed:
                continue  # Skip open leads when filtering for inactive cases
        
        # Apply tenure filter using tenure field from API
        if tenure_filter:
            app_tenure = app.get('tenure', 0)
            try:
                # Convert tenure_filter to integer for comparison
                filter_tenure = int(tenure_filter)
                if app_tenure != filter_tenure:
                    continue
            except (ValueError, TypeError):
                # If tenure_filter is not a valid integer, skip this filter
                print(f"⚠️  Invalid tenure filter value: {tenure_filter}")
                continue
        
        if state_filter:
            app_state = app.get('state', '')
            if app_state != state_filter:
                continue
        
        if city_filter:
            app_city = app.get('city', '')
            if app_city != city_filter:
                continue
        
        # Count this as a filtered application
        filtered_applications += 1
        
        # Handle different field names from Blinkr API
        sanction_amount = float(app.get('sanction_amount', app.get('sanctionAmount', app.get('loan_amount', 0))) or 0)
        disbursed_amount = float(app.get('disbursed_amount', app.get('disbursal_amt', app.get('disbursalAmount', 0))) or 0)
        processing_fee = float(app.get('processing_fee', app.get('processingFee', app.get('pf_amount', 0))) or 0)
        interest_amount = float(app.get('interest_amount', app.get('interestAmount', 0)) or 0)
        repayment_amount = float(app.get('repayment_amount', app.get('repaymentAmount', 0)) or 0)
        
        total_sanction_amount += sanction_amount
        total_disbursed_amount += disbursed_amount
        total_pf_amount += processing_fee
        total_interest_amount += interest_amount
        total_repayment_amount += repayment_amount
    
    # Use filtered count for total applications
    total_applications = filtered_applications
    avg_disbursal = total_disbursed_amount / total_applications if total_applications > 0 else 0
    
    base_data = {
        "total_applications": total_applications,
        "total_sanction_amount": round(total_sanction_amount, 2),
        "total_disbursed_amount": round(total_disbursed_amount, 2),
        "total_pf_amount": round(total_pf_amount, 2),
        "total_interest_amount": round(total_interest_amount, 2),
        "total_repayment_amount": round(total_repayment_amount, 2),
        "avg_disbursal": round(avg_disbursal, 2)
    }
    
    print(f"Calculated summary from Blinkr API: {total_applications} applications")
    print(f"Total disbursed amount: ₹{total_disbursed_amount:,}")
    
    return JsonResponse(base_data)

@csrf_exempt
def charts_data(request):
    """API endpoint for charts data with date filtering (using Blinkr API)"""
    # Check authentication
    if not request.session.get('authenticated'):
        return JsonResponse({"error": "Authentication required"}, status=401)
    
    # Get date parameters
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    # Get filter parameters
    reloan_filter = request.GET.get('reloan', '')
    active_filter = request.GET.get('active', '')
    tenure_filter = request.GET.get('tenure', '')
    state_filter = request.GET.get('state', '')
    city_filter = request.GET.get('city', '')
    
    if not start_date or not end_date:
        return JsonResponse({"error": "start_date and end_date required"}, status=400)
    
    print(f"Charts data requested - Start: {start_date}, End: {end_date}")
    print(f"Filters: Reloan={reloan_filter}, Active={active_filter}, Tenure={tenure_filter}, State={state_filter}, City={city_filter}")
    
    # Use Blinkr API data instead of mock data
    apps = fetch_blinkr_data(start_date, end_date)
    
    if not apps:
        return JsonResponse({
            "state_data": [{"state": "No Data", "value": 0, "percentage": 0}],
            "city_data": [{"city": "No Data", "value": 0, "percentage": 0}]
        })
    
    print(f"Charts: Processing {len(apps)} applications from Blinkr API")
    
    # Calculate state and city data from Blinkr API data
    state_map = {}
    city_map = {}
    
    for app in apps:
        # Apply filters if specified
        if reloan_filter:
            is_reloan_case = app.get('is_reloan_case', False)
            if reloan_filter == 'reloan' and not is_reloan_case:
                continue
            elif reloan_filter == 'new' and is_reloan_case:
                continue
        
        # Apply active filter using is_lead_closed field from API
        if active_filter:
            is_lead_closed = app.get('is_lead_closed', False)
            if active_filter == 'active' and is_lead_closed:
                continue  # Skip closed leads when filtering for active cases
            elif active_filter == 'inactive' and not is_lead_closed:
                continue  # Skip open leads when filtering for inactive cases
        
        # Apply tenure filter using tenure field from API
        if tenure_filter:
            app_tenure = app.get('tenure', 0)
            try:
                # Convert tenure_filter to integer for comparison
                filter_tenure = int(tenure_filter)
                if app_tenure != filter_tenure:
                    continue
            except (ValueError, TypeError):
                # If tenure_filter is not a valid integer, skip this filter
                print(f"⚠️  Invalid tenure filter value: {tenure_filter}")
                continue
        
        if state_filter:
            app_state = app.get('state', '')
            if app_state != state_filter:
                continue
        
        if city_filter:
            app_city = app.get('city', '')
            if app_city != city_filter:
                continue
        
        # Handle different field names from Blinkr API
        state = app.get('state', 'Unknown')
        city = app.get('city', 'Unknown')
        disbursed_amount = float(app.get('disbursed_amount', app.get('disbursal_amt', app.get('disbursalAmount', 0))) or 0)
        
        # Aggregate state data
        if state in state_map:
            state_map[state] += disbursed_amount
        else:
            state_map[state] = disbursed_amount
        
        # Aggregate city data
        if city in city_map:
            city_map[city] += disbursed_amount
        else:
            city_map[city] = disbursed_amount
    
    # Convert to chart format
    total_state_amount = sum(state_map.values())
    state_data = [
        {
            "state": state,
            "value": amount,
            "percentage": round((amount / total_state_amount) * 100, 1) if total_state_amount > 0 else 0
        }
        for state, amount in state_map.items()
    ]
    
    total_city_amount = sum(city_map.values())
    city_data = [
        {
            "city": city,
            "value": amount,
            "percentage": round((amount / total_city_amount) * 100, 1) if total_city_amount > 0 else 0
        }
        for city, amount in city_map.items()
    ]
    
    base_data = {
        "state_data": state_data,
        "city_data": city_data
    }
    
    return JsonResponse(base_data)

@csrf_exempt
def filtered_charts_data(request):
    """API endpoint for filtered chart data based on selected filters"""
    # Get filter parameters
    state_filter = request.GET.get('state', '')
    city_filter = request.GET.get('city', '')
    reloan_filter = request.GET.get('reloan', '')
    active_filter = request.GET.get('active', '')
    tenure_filter = request.GET.get('tenure', '')
    
    # Get date parameters for API call
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    if not start_date or not end_date:
        return JsonResponse({"error": "start_date and end_date required"}, status=400)
    
    print(f"Filtered charts data requested - Start: {start_date}, End: {end_date}")
    print(f"Filters: State={state_filter}, City={city_filter}, Reloan={reloan_filter}")
    
    # Use Blinkr API data instead of mock data
    apps = fetch_blinkr_data(start_date, end_date)
    
    if not apps:
        return JsonResponse({
            "state_data": [{"state": "No Data", "value": 0, "percentage": 0}],
            "city_data": [{"city": "No Data", "value": 0, "percentage": 0}],
            "filters_applied": {
                'state': state_filter,
                'city': city_filter,
                'reloan': reloan_filter,
                'active': active_filter,
                'tenure': tenure_filter
            }
        })
    
    print(f"Filtered charts: Processing {len(apps)} applications from Blinkr API")
    
    # Calculate state and city data from Blinkr API data
    state_map = {}
    city_map = {}
    
    for app in apps:
        # Handle different field names from Blinkr API
        state = app.get('state', 'Unknown')
        city = app.get('city', 'Unknown')
        disbursed_amount = float(app.get('disbursed_amount', app.get('disbursal_amt', app.get('disbursalAmount', 0))) or 0)
        
        # Apply filters if specified
        if state_filter and state != state_filter:
            continue
        if city_filter and city != city_filter:
            continue
        
        # Apply reloan filter using is_reloan_case field from API
        if reloan_filter:
            is_reloan_case = app.get('is_reloan_case', False)
            if reloan_filter == 'reloan' and not is_reloan_case:
                continue
            elif reloan_filter == 'new' and is_reloan_case:
                continue
        
        # Aggregate state data
        if state in state_map:
            state_map[state] += disbursed_amount
        else:
            state_map[state] = disbursed_amount
        
        # Aggregate city data
        if city in city_map:
            city_map[city] += disbursed_amount
        else:
            city_map[city] = disbursed_amount
    
    # Convert to chart format
    total_state_amount = sum(state_map.values())
    state_data = [
        {
            "state": state,
            "value": amount,
            "percentage": round((amount / total_state_amount) * 100, 1) if total_state_amount > 0 else 0
        }
        for state, amount in state_map.items()
    ]
    
    total_city_amount = sum(city_map.values())
    city_data = [
        {
            "city": city,
            "value": amount,
            "percentage": round((amount / total_city_amount) * 100, 1) if total_city_amount > 0 else 0
        }
        for city, amount in city_map.items()
    ]
    
    # Ensure we have data to return
    if not state_data:
        state_data = [{'state': 'No Data', 'value': 0, 'percentage': 0}]
    if not city_data:
        city_data = [{'city': 'No Data', 'value': 0, 'percentage': 0}]
    
    return JsonResponse({
        'state_data': state_data,
        'city_data': city_data,
        'filters_applied': {
            'state': state_filter,
            'city': city_filter,
            'reloan': reloan_filter,
            'active': active_filter,
            'tenure': tenure_filter
        }
    })

@csrf_exempt
def table_data(request):
    """API endpoint for table data with date filtering (using Blinkr API)"""
    # Check authentication
    if not request.session.get('authenticated'):
        return JsonResponse({"error": "Authentication required"}, status=401)
    
    # Get date parameters
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    # Get pagination parameters
    page = int(request.GET.get('page', 1))
    per_page = int(request.GET.get('per_page', 10))
    
    # Get search parameter
    search_term = request.GET.get('search', '').strip()
    
    # Get filter parameters
    reloan_filter = request.GET.get('reloan', '')
    active_filter = request.GET.get('active', '')
    tenure_filter = request.GET.get('tenure', '')
    state_filter = request.GET.get('state', '')
    city_filter = request.GET.get('city', '')
    
    if not start_date or not end_date:
        return JsonResponse({"error": "start_date and end_date required"}, status=400)
    
    print(f"Table data requested - Start: {start_date}, End: {end_date}, Page: {page}, Per Page: {per_page}, Search: '{search_term}'")
    print(f"Filters: Reloan={reloan_filter}, Active={active_filter}, Tenure={tenure_filter}, State={state_filter}, City={city_filter}")
    
    # Use Blinkr API data instead of mock data
    apps = fetch_blinkr_data(start_date, end_date)
    
    if not apps:
        return JsonResponse({
            "applications": [],
            "total_pages": 0,
            "current_page": 1,
            "total_items": 0,
            "per_page": per_page
        })
    
    print(f"Table: Processing {len(apps)} applications from Blinkr API")
    
    # Process applications for table display
    table_applications = []
    for i, app in enumerate(apps):
        # Debug: Print the first few applications to see field names
        if i < 3:
            print(f"🔍 Sample app {i}: {app}")
        
        # Handle different field names from Blinkr API
        disbursal_date = app.get('disbursal_date', app.get('disbursalDate', app.get('date', 'N/A')))
        full_name = app.get('full_name', app.get('fullName', app.get('name', app.get('customer_name', app.get('applicant_name', 'N/A')))))
        sanction_amount = float(app.get('sanction_amount', app.get('sanctionAmount', app.get('loan_amount', 0))) or 0)
        disbursed_amount = float(app.get('disbursed_amount', app.get('disbursal_amt', app.get('disbursalAmount', 0))) or 0)
        processing_fee = float(app.get('processing_fee', app.get('processingFee', app.get('pf_amount', 0))) or 0)
        interest_amount = float(app.get('interest_amount', app.get('interestAmount', 0)) or 0)
        repayment_amount = float(app.get('repayment_amount', app.get('repaymentAmount', 0)) or 0)
        
        # Apply search filter if search term exists
        if search_term:
            # Search in full name (case-insensitive)
            if search_term.lower() not in full_name.lower():
                continue  # Skip this application if it doesn't match search
        
        # Apply reloan filter using is_reloan_case field from API
        if reloan_filter:
            is_reloan_case = app.get('is_reloan_case', False)
            if reloan_filter == 'reloan' and not is_reloan_case:
                continue
            elif reloan_filter == 'new' and is_reloan_case:
                continue
        
        # Apply active filter using is_lead_closed field from API
        if active_filter:
            is_lead_closed = app.get('is_lead_closed', False)
            if active_filter == 'active' and is_lead_closed:
                continue  # Skip closed leads when filtering for active cases
            elif active_filter == 'inactive' and not is_lead_closed:
                continue  # Skip open leads when filtering for inactive cases
        
        # Apply tenure filter using tenure field from API
        if tenure_filter:
            app_tenure = app.get('tenure', 0)
            try:
                # Convert tenure_filter to integer for comparison
                filter_tenure = int(tenure_filter)
                if app_tenure != filter_tenure:
                    continue
            except (ValueError, TypeError):
                # If tenure_filter is not a valid integer, skip this filter
                print(f"⚠️  Invalid tenure filter value: {tenure_filter}")
                continue
        
        # Apply state filter
        if state_filter:
            app_state = app.get('state', '')
            if app_state != state_filter:
                continue
        
        # Apply city filter
        if city_filter:
            app_city = app.get('city', '')
            if app_city != city_filter:
                continue
        
        table_applications.append({
            "id": i + 1,
            "disbursal_date": disbursal_date,
            "full_name": full_name,
            "sanction_amount": sanction_amount,
            "disbursed_amount": disbursed_amount,
            "processing_fee": processing_fee,
            "interest_amount": interest_amount,
            "repayment_amount": repayment_amount
        })
    
    print(f"🔍 After search filtering: {len(table_applications)} applications match search term '{search_term}'")
    
    # Calculate pagination
    total_items = len(table_applications)
    total_pages = (total_items + per_page - 1) // per_page  # Ceiling division
    
    # Ensure page is within valid range
    if page < 1:
        page = 1
    elif page > total_pages:
        page = total_pages
    
    # Get the slice of data for the current page
    start_index = (page - 1) * per_page
    end_index = start_index + per_page
    page_data = table_applications[start_index:end_index]
    
    base_data = {
        "applications": page_data,
        "total_pages": total_pages,
        "current_page": page,
        "total_items": total_items,
        "per_page": per_page,
        "start_index": start_index + 1,
        "end_index": min(end_index, total_items)
    }
    
    print(f"📊 Returning {len(page_data)} applications for page {page} of {total_pages}")
    print(f"📄 Showing items {start_index + 1} to {min(end_index, total_items)} of {total_items}")
    if page_data:
        print(f"🔍 First application sample: {page_data[0]}")
    
    return JsonResponse(base_data)

@csrf_exempt
def date_range(request):
    """API endpoint to get the available date range for disbursal data"""
    # For now, return a reasonable date range
    # In production, this would query your database for the actual date range
    data = {
        "min_date": "2023-01-01",
        "max_date": "2025-12-31",
        "available_dates": []
    }
    
    print(f"Date range requested - Min: {data['min_date']}, Max: {data['max_date']}")
    return JsonResponse(data)

@csrf_exempt
def distinct_values(request):
    """API endpoint to get distinct values for filters from the API data with cascading filter support"""
    print(f"🔍 Distinct values endpoint accessed")
    print(f"🔍 Session data: {dict(request.session)}")
    print(f"🔍 Session ID: {request.session.session_key}")
    print(f"🔍 Authenticated: {request.session.get('authenticated')}")
    
    if not request.session.get('authenticated'):
        print("❌ User not authenticated in distinct_values endpoint")
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    
    # Get current date range and ALL current filter values from request
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')
    reloan_filter = request.GET.get('reloan', '')
    active_filter = request.GET.get('active', '')
    tenure_filter = request.GET.get('tenure', '')
    state_filter = request.GET.get('state', '')
    city_filter = request.GET.get('city', '')
    
    print(f"🔍 Request parameters - start_date: {start_date}, end_date: {end_date}")
    print(f"🔍 Current filters - reloan: {reloan_filter}, active: {active_filter}, tenure: {tenure_filter}, state: {state_filter}, city: {city_filter}")
    
    if not start_date or not end_date:
        print("❌ Missing start_date or end_date parameters")
        return JsonResponse({'error': 'Start date and end date are required'}, status=400)
    
    print(f"🔍 Fetching distinct values for date range: {start_date} to {end_date}")
    
    # Fetch data from Blinkr API
    apps = fetch_blinkr_data(start_date, end_date)
    
    print(f"🔍 Blinkr API returned {len(apps) if apps else 0} applications")
    
    if not apps:
        print("⚠️  No data returned from API for distinct values")
        return JsonResponse({
            'tenures': [],
            'states': [],
            'cities': []
        })
    
    # Apply current filters to get filtered data first
    filtered_apps = []
    for app in apps:
        # Apply reloan filter
        if reloan_filter:
            is_reloan_case = app.get('is_reloan_case', False)
            if reloan_filter == 'reloan' and not is_reloan_case:
                continue
            elif reloan_filter == 'new' and is_reloan_case:
                continue
        
        # Apply active filter
        if active_filter:
            is_lead_closed = app.get('is_lead_closed', False)
            if active_filter == 'active' and is_lead_closed:
                continue
            elif active_filter == 'inactive' and not is_lead_closed:
                continue
        
        # Apply tenure filter
        if tenure_filter:
            app_tenure = app.get('tenure', 0)
            try:
                filter_tenure = int(tenure_filter)
                if app_tenure != filter_tenure:
                    continue
            except (ValueError, TypeError):
                continue
        
        # Apply state filter
        if state_filter:
            app_state = app.get('state', '')
            if app_state != state_filter:
                continue
        
        # Apply city filter
        if city_filter:
            app_city = app.get('city', '')
            if app_city != city_filter:
                continue
        
        filtered_apps.append(app)
    
    print(f"🔍 After applying filters: {len(filtered_apps)} applications remain")
    
    # Extract distinct values from the FILTERED data
    tenures = set()
    states = set()
    cities = set()
    
    for app in filtered_apps:
        # Extract tenure values
        tenure = app.get('tenure', 0)
        if tenure and tenure > 0:
            tenures.add(tenure)
        
        # Extract state values
        state = app.get('state', '')
        if state:
            states.add(state)
        
        # Extract city values
        city = app.get('city', '')
        if city:
            cities.add(city)
    
    # Convert to sorted lists
    tenures_list = sorted(list(tenures))
    states_list = sorted(list(states))
    cities_list = sorted(list(cities))
    
    print(f"🔍 Distinct values found from filtered data:")
    print(f"   - Tenures: {tenures_list}")
    print(f"   - States: {states_list}")
    print(f"   - Cities: {cities_list}")
    
    # Sample some filtered data to debug
    if filtered_apps:
        print(f"🔍 Sample filtered application data:")
        sample_app = filtered_apps[0]
        print(f"   - Sample app keys: {list(sample_app.keys())}")
        print(f"   - Sample app state: {sample_app.get('state', 'NOT_FOUND')}")
        print(f"   - Sample app city: {sample_app.get('city', 'NOT_FOUND')}")
        print(f"   - Sample app tenure: {sample_app.get('tenure', 'NOT_FOUND')}")
    
    return JsonResponse({
        'tenures': tenures_list,
        'states': states_list,
        'cities': cities_list
    })
