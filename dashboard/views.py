from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime, timedelta
import random

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
        return render(request, 'dashboard/dashboard.html')
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
    """Logout view"""
    request.session.pop('authenticated', None)
    return redirect('/login/')

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
    # Get date parameters
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    print(f"Summary data requested - Start: {start_date}, End: {end_date}")
    
    # Mock data with disbursal dates - replace with your actual API call
    # In production, this would come from your database
    mock_applications = [
        {
            "disbursal_date": "2025-01-15",
            "sanction_amount": 50000,
            "disbursed_amount": 45000,
            "processing_fee": 5000,
            "interest_amount": 3000,
            "repayment_amount": 53000
        },
        {
            "disbursal_date": "2025-01-16",
            "sanction_amount": 75000,
            "disbursed_amount": 70000,
            "processing_fee": 7500,
            "interest_amount": 4500,
            "repayment_amount": 79000
        },
        {
            "disbursal_date": "2025-01-17",
            "sanction_amount": 60000,
            "disbursed_amount": 55000,
            "processing_fee": 6000,
            "interest_amount": 3500,
            "repayment_amount": 64500
        },
        {
            "disbursal_date": "2025-01-18",
            "sanction_amount": 80000,
            "disbursed_amount": 75000,
            "processing_fee": 8000,
            "interest_amount": 5000,
            "repayment_amount": 88000
        },
        {
            "disbursal_date": "2025-01-19",
            "sanction_amount": 45000,
            "disbursed_amount": 40000,
            "processing_fee": 4500,
            "interest_amount": 2500,
            "repayment_amount": 47000
        },
        {
            "disbursal_date": "2025-07-26",
            "sanction_amount": 55000,
            "disbursed_amount": 50000,
            "processing_fee": 5500,
            "interest_amount": 3200,
            "repayment_amount": 58700
        },
        {
            "disbursal_date": "2025-07-27",
            "sanction_amount": 65000,
            "disbursed_amount": 60000,
            "processing_fee": 6500,
            "interest_amount": 3800,
            "repayment_amount": 70300
        },
        {
            "disbursal_date": "2025-08-01",
            "sanction_amount": 70000,
            "disbursed_amount": 65000,
            "processing_fee": 7000,
            "interest_amount": 4200,
            "repayment_amount": 76200
        },
        {
            "disbursal_date": "2025-08-15",
            "sanction_amount": 85000,
            "disbursed_amount": 80000,
            "processing_fee": 8500,
            "interest_amount": 5000,
            "repayment_amount": 93500
        },
        {
            "disbursal_date": "2025-08-20",
            "sanction_amount": 90000,
            "disbursed_amount": 85000,
            "processing_fee": 9000,
            "interest_amount": 5500,
            "repayment_amount": 99500
        }
    ]
    
    if start_date and end_date:
        # Filter applications based on disbursal_date range
        filtered_applications = [
            app for app in mock_applications 
            if start_date <= app["disbursal_date"] <= end_date
        ]
        
        print(f"Filtered applications count: {len(filtered_applications)}")
        
        if filtered_applications:
            # Calculate summary from filtered data
            total_applications = len(filtered_applications)
            total_sanction_amount = sum(app["sanction_amount"] for app in filtered_applications)
            total_disbursed_amount = sum(app["disbursed_amount"] for app in filtered_applications)
            total_pf_amount = sum(app["processing_fee"] for app in filtered_applications)
            total_interest_amount = sum(app["interest_amount"] for app in filtered_applications)
            total_repayment_amount = sum(app["repayment_amount"] for app in filtered_applications)
            avg_disbursal = total_disbursed_amount / total_applications if total_applications > 0 else 0
            
            base_data = {
                "total_applications": total_applications,
                "total_sanction_amount": total_sanction_amount,
                "total_disbursed_amount": total_disbursed_amount,
                "total_pf_amount": total_pf_amount,
                "total_interest_amount": total_interest_amount,
                "total_repayment_amount": total_repayment_amount,
                "avg_disbursal": round(avg_disbursal, 2)
            }
            
            print(f"Calculated repayment amount for date range: ₹{total_repayment_amount:,}")
            print(f"Breakdown: {len(filtered_applications)} applications with repayment amounts:")
            for app in filtered_applications:
                print(f"  - {app['disbursal_date']}: ₹{app['repayment_amount']:,} ({app['full_name']})")
        else:
            # No data for selected date range
            base_data = {
                "total_applications": 0,
                "total_sanction_amount": 0,
                "total_disbursed_amount": 0,
                "total_pf_amount": 0,
                "total_interest_amount": 0,
                "total_repayment_amount": 0,
                "avg_disbursal": 0
            }
            print("No data found for selected date range")
    else:
        # No date range provided, return all data
        total_applications = len(mock_applications)
        total_sanction_amount = sum(app["sanction_amount"] for app in mock_applications)
        total_disbursed_amount = sum(app["disbursed_amount"] for app in mock_applications)
        total_pf_amount = sum(app["processing_fee"] for app in mock_applications)
        total_interest_amount = sum(app["interest_amount"] for app in mock_applications)
        total_repayment_amount = sum(app["repayment_amount"] for app in mock_applications)
        avg_disbursal = total_disbursed_amount / total_applications if total_applications > 0 else 0
        
        base_data = {
            "total_applications": total_applications,
            "total_sanction_amount": total_sanction_amount,
            "total_disbursed_amount": total_disbursed_amount,
            "total_pf_amount": total_pf_amount,
            "total_interest_amount": total_interest_amount,
            "total_repayment_amount": total_repayment_amount,
            "avg_disbursal": round(avg_disbursal, 2)
        }
    
    return JsonResponse(base_data)

@csrf_exempt
def charts_data(request):
    """API endpoint for charts data with date filtering"""
    # Get date parameters
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    print(f"Charts data requested - Start: {start_date}, End: {end_date}")
    
    # Mock data with disbursal dates - replace with your actual API call
    # In production, this would come from your database
    mock_applications = [
        {
            "disbursal_date": "2025-01-15",
            "state": "Delhi",
            "city": "Delhi",
            "disbursed_amount": 45000
        },
        {
            "disbursal_date": "2025-01-16",
            "state": "Haryana",
            "city": "Gurugram",
            "disbursed_amount": 70000
        },
        {
            "disbursal_date": "2025-01-17",
            "state": "Uttar Pradesh",
            "city": "Noida",
            "disbursed_amount": 55000
        },
        {
            "disbursal_date": "2025-01-18",
            "state": "Delhi",
            "city": "Central Delhi",
            "disbursed_amount": 75000
        },
        {
            "disbursal_date": "2025-01-19",
            "state": "Haryana",
            "city": "Faridabad",
            "disbursed_amount": 40000
        },
        {
            "disbursal_date": "2025-07-26",
            "state": "Maharashtra",
            "city": "Mumbai Suburban",
            "disbursed_amount": 50000
        },
        {
            "disbursal_date": "2025-07-27",
            "state": "Telangana",
            "city": "Hyderabad",
            "disbursed_amount": 60000
        },
        {
            "disbursal_date": "2025-08-01",
            "state": "Delhi",
            "city": "West Delhi",
            "disbursed_amount": 65000
        },
        {
            "disbursal_date": "2025-08-15",
            "state": "Uttar Pradesh",
            "city": "Lucknow",
            "disbursed_amount": 80000
        },
        {
            "disbursal_date": "2025-08-20",
            "state": "Haryana",
            "city": "Ghaziabad",
            "disbursed_amount": 85000
        }
    ]
    
    if start_date and end_date:
        # Filter applications based on disbursal_date range
        filtered_applications = [
            app for app in mock_applications 
            if start_date <= app["disbursal_date"] <= end_date
        ]
        
        print(f"Charts: Filtered applications count: {len(filtered_applications)}")
        
        if filtered_applications:
            # Calculate state and city data from filtered applications
            state_map = {}
            city_map = {}
            
            for app in filtered_applications:
                # Aggregate state data
                state = app["state"]
                if state in state_map:
                    state_map[state] += app["disbursed_amount"]
                else:
                    state_map[state] = app["disbursed_amount"]
                
                # Aggregate city data
                city = app["city"]
                if city in city_map:
                    city_map[city] += app["disbursed_amount"]
                else:
                    city_map[city] = app["disbursed_amount"]
            
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
        else:
            # No data for selected date range
            base_data = {
                "state_data": [{"state": "No Data", "value": 0, "percentage": 0}],
                "city_data": [{"city": "No Data", "value": 0, "percentage": 0}]
            }
    else:
        # No date range provided, return default data
        base_data = {
            "state_data": [
                {"state": "Delhi", "value": 150000, "percentage": 45.2},
                {"state": "Haryana", "value": 120000, "percentage": 36.1},
                {"state": "Uttar Pradesh", "value": 62000, "percentage": 18.7}
            ],
            "city_data": [
                {"city": "Gurugram", "value": 80000, "percentage": 24.1},
                {"city": "Delhi", "value": 75000, "percentage": 22.6},
                {"city": "Noida", "value": 65000, "percentage": 19.6},
                {"city": "Faridabad", "value": 45000, "percentage": 13.6},
                {"city": "Ghaziabad", "value": 35000, "percentage": 10.5},
                {"city": "Others", "value": 32000, "percentage": 9.6}
            ]
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
    
    # Base data - in a real application, this would come from database queries
    all_state_data = {
        'Maharashtra': [
            {'state': 'Maharashtra', 'value': 137000, 'percentage': 29.15},
            {'state': 'Maharashtra (New)', 'value': 89000, 'percentage': 19.0},
            {'state': 'Maharashtra (Reloan)', 'value': 48000, 'percentage': 10.15}
        ],
        'Haryana': [
            {'state': 'Haryana', 'value': 120000, 'percentage': 25.57},
            {'state': 'Haryana (New)', 'value': 75000, 'percentage': 16.0},
            {'state': 'Haryana (Reloan)', 'value': 45000, 'percentage': 9.57}
        ],
        'Telangana': [
            {'state': 'Telangana', 'value': 93000, 'percentage': 19.8},
            {'state': 'Telangana (New)', 'value': 62000, 'percentage': 13.2},
            {'state': 'Telangana (Reloan)', 'value': 31000, 'percentage': 6.6}
        ],
        'Uttar Pradesh': [
            {'state': 'Uttar Pradesh', 'value': 67000, 'percentage': 14.29},
            {'state': 'Uttar Pradesh (New)', 'value': 42000, 'percentage': 8.9},
            {'state': 'Uttar Pradesh (Reloan)', 'value': 25000, 'percentage': 5.39}
        ],
        'Delhi': [
            {'state': 'Delhi', 'value': 53000, 'percentage': 11.2},
            {'state': 'Delhi (New)', 'value': 35000, 'percentage': 7.4},
            {'state': 'Delhi (Reloan)', 'value': 18000, 'percentage': 3.8}
        ]
    }
    
    all_city_data = {
        'Gurugram': [
            {'city': 'Gurugram', 'value': 120000, 'percentage': 25.57},
            {'city': 'Gurugram (New)', 'value': 75000, 'percentage': 16.0},
            {'city': 'Gurugram (Reloan)', 'value': 45000, 'percentage': 9.57}
        ],
        'Hyderabad': [
            {'city': 'Hyderabad', 'value': 80000, 'percentage': 17.07},
            {'city': 'Hyderabad (New)', 'value': 52000, 'percentage': 11.1},
            {'city': 'Hyderabad (Reloan)', 'value': 28000, 'percentage': 6.0}
        ],
        'Mumbai Suburban': [
            {'city': 'Mumbai Suburban', 'value': 71000, 'percentage': 15.22},
            {'city': 'Mumbai Suburban (New)', 'value': 48000, 'percentage': 10.2},
            {'city': 'Mumbai Suburban (Reloan)', 'value': 23000, 'percentage': 5.0}
        ],
        'Pune': [
            {'city': 'Pune', 'value': 65000, 'percentage': 13.9},
            {'city': 'Pune (New)', 'value': 42000, 'percentage': 9.0},
            {'city': 'Pune (Reloan)', 'value': 23000, 'percentage': 4.9}
        ],
        'Lucknow': [
            {'city': 'Lucknow', 'value': 35000, 'percentage': 7.47},
            {'city': 'Lucknow (New)', 'value': 22000, 'percentage': 4.7},
            {'city': 'Lucknow (Reloan)', 'value': 13000, 'percentage': 2.77}
        ],
        'Central Delhi': [
            {'city': 'Central Delhi', 'value': 32000, 'percentage': 6.83},
            {'city': 'Central Delhi (New)', 'value': 20000, 'percentage': 4.3},
            {'city': 'Central Delhi (Reloan)', 'value': 12000, 'percentage': 2.53}
        ],
        'West Delhi': [
            {'city': 'West Delhi', 'value': 19000, 'percentage': 4.05},
            {'city': 'West Delhi (New)', 'value': 12000, 'percentage': 2.6},
            {'city': 'West Delhi (Reloan)', 'value': 7000, 'percentage': 1.45}
        ],
        'Ghaziabad': [
            {'city': 'Ghaziabad', 'value': 13000, 'percentage': 2.73},
            {'city': 'Ghaziabad (New)', 'value': 8000, 'percentage': 1.7},
            {'city': 'Ghaziabad (Reloan)', 'value': 5000, 'percentage': 1.03}
        ]
    }
    
    # Apply filters and generate filtered data
    if state_filter:
        # Filter by specific state
        state_data = all_state_data.get(state_filter, [])
        if city_filter and city_filter in all_city_data:
            # Further filter by city
            city_data = all_city_data[city_filter]
        else:
            # Show cities within the selected state
            city_data = []
            for city, city_info in all_city_data.items():
                if any(city in state_filter for state in ['Delhi', 'Haryana', 'Uttar Pradesh'] if city in ['Gurugram', 'Central Delhi', 'West Delhi', 'Ghaziabad']):
                    city_data.extend(city_info)
                elif state_filter == 'Maharashtra' and city in ['Mumbai Suburban', 'Pune']:
                    city_data.extend(city_info)
                elif state_filter == 'Telangana' and city == 'Hyderabad':
                    city_data.extend(city_info)
                elif state_filter == 'Uttar Pradesh' and city == 'Lucknow':
                    city_data.extend(city_info)
    elif city_filter:
        # Filter by specific city only
        city_data = all_city_data.get(city_filter, [])
        # Determine state from city
        state_mapping = {
            'Gurugram': 'Haryana',
            'Hyderabad': 'Telangana',
            'Mumbai Suburban': 'Maharashtra',
            'Pune': 'Maharashtra',
            'Lucknow': 'Uttar Pradesh',
            'Central Delhi': 'Delhi',
            'West Delhi': 'Delhi',
            'Ghaziabad': 'Uttar Pradesh'
        }
        state_data = all_state_data.get(state_mapping.get(city_filter, ''), [])
    else:
        # No filters applied, return default data
        state_data = [
            {'state': 'Maharashtra', 'value': 137000, 'percentage': 29.15},
            {'state': 'Haryana', 'value': 120000, 'percentage': 25.57},
            {'state': 'Telangana', 'value': 93000, 'percentage': 19.8},
            {'state': 'Uttar Pradesh', 'value': 67000, 'percentage': 14.29},
            {'state': 'Delhi', 'value': 53000, 'percentage': 11.2}
        ]
        
        city_data = [
            {'city': 'Gurugram', 'value': 120000, 'percentage': 25.57},
            {'city': 'Hyderabad', 'value': 80000, 'percentage': 17.07},
            {'city': 'Mumbai Suburban', 'value': 71000, 'percentage': 15.22},
            {'city': 'Pune', 'value': 65000, 'percentage': 13.9},
            {'city': 'Lucknow', 'value': 35000, 'percentage': 7.47},
            {'city': 'Central Delhi', 'value': 32000, 'percentage': 6.83},
            {'city': 'West Delhi', 'value': 19000, 'percentage': 4.05},
            {'city': 'Ghaziabad', 'value': 13000, 'percentage': 2.73}
        ]
    
    # Apply additional filters (reloan, active, tenure) if needed
    # In a real application, these would filter the actual data
    if reloan_filter:
        # Filter by reloan case
        if reloan_filter == 'new':
            state_data = [item for item in state_data if 'New' in item['state'] or 'New' not in item['state'] and 'Reloan' not in item['state']]
            city_data = [item for item in city_data if 'New' in item['city'] or 'New' not in item['city'] and 'Reloan' not in item['city']]
        elif reloan_filter == 'reloan':
            state_data = [item for item in state_data if 'Reloan' in item['state']]
            city_data = [item for item in city_data if 'Reloan' in item['city']]
    
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
    """API endpoint for table data with date filtering"""
    # Get date parameters
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    print(f"Table data requested - Start: {start_date}, End: {end_date}")
    
    # Mock data - replace with your actual API call
    # In production, filter this data based on start_date and end_date
    base_data = {
        "applications": [
            {
                "id": 1,
                "disbursal_date": "2025-01-15",
                "full_name": "John Doe",
                "sanction_amount": 50000,
                "disbursed_amount": 45000,
                "processing_fee": 5000,
                "interest_amount": 3000,
                "repayment_amount": 53000
            },
            {
                "id": 2,
                "disbursal_date": "2025-01-16",
                "full_name": "Jane Smith",
                "sanction_amount": 75000,
                "disbursed_amount": 70000,
                "processing_fee": 7500,
                "interest_amount": 4500,
                "repayment_amount": 79000
            }
        ],
        "total_pages": 1,
        "current_page": 1,
        "total_items": 2
    }
    
    # Mock data with disbursal dates - replace with your actual API call
    # In production, this would come from your database
    mock_applications = [
        {
            "id": 1,
            "disbursal_date": "2025-01-15",
            "full_name": "John Doe",
            "sanction_amount": 50000,
            "disbursed_amount": 45000,
            "processing_fee": 5000,
            "interest_amount": 3000,
            "repayment_amount": 53000
        },
        {
            "id": 2,
            "disbursal_date": "2025-01-16",
            "full_name": "Jane Smith",
            "sanction_amount": 75000,
            "disbursed_amount": 70000,
            "processing_fee": 7500,
            "interest_amount": 4500,
            "repayment_amount": 79000
        },
        {
            "id": 3,
            "disbursal_date": "2025-01-17",
            "full_name": "Mike Johnson",
            "sanction_amount": 60000,
            "disbursed_amount": 55000,
            "processing_fee": 6000,
            "interest_amount": 3500,
            "repayment_amount": 64500
        },
        {
            "id": 4,
            "disbursal_date": "2025-01-18",
            "full_name": "Sarah Wilson",
            "sanction_amount": 80000,
            "disbursed_amount": 75000,
            "processing_fee": 8000,
            "interest_amount": 5000,
            "repayment_amount": 88000
        },
        {
            "id": 5,
            "disbursal_date": "2025-01-19",
            "full_name": "David Brown",
            "sanction_amount": 45000,
            "disbursed_amount": 40000,
            "processing_fee": 4500,
            "interest_amount": 2500,
            "repayment_amount": 47000
        },
        {
            "id": 6,
            "disbursal_date": "2025-07-26",
            "full_name": "Emily Davis",
            "sanction_amount": 55000,
            "disbursed_amount": 50000,
            "processing_fee": 5500,
            "interest_amount": 3200,
            "repayment_amount": 58700
        },
        {
            "id": 7,
            "disbursal_date": "2025-07-27",
            "full_name": "Robert Miller",
            "sanction_amount": 65000,
            "disbursed_amount": 60000,
            "processing_fee": 6500,
            "interest_amount": 3800,
            "repayment_amount": 70300
        },
        {
            "id": 8,
            "disbursal_date": "2025-08-01",
            "full_name": "Lisa Garcia",
            "sanction_amount": 70000,
            "disbursed_amount": 65000,
            "processing_fee": 7000,
            "interest_amount": 4200,
            "repayment_amount": 76200
        },
        {
            "id": 9,
            "disbursal_date": "2025-07-15",
            "full_name": "James Rodriguez",
            "sanction_amount": 85000,
            "disbursed_amount": 80000,
            "processing_fee": 8500,
            "interest_amount": 5000,
            "repayment_amount": 93500
        },
        {
            "id": 10,
            "disbursal_date": "2025-08-20",
            "full_name": "Maria Martinez",
            "sanction_amount": 90000,
            "disbursed_amount": 85000,
            "processing_fee": 9000,
            "interest_amount": 5500,
            "repayment_amount": 99500
        }
    ]
    
    if start_date and end_date:
        # Filter applications based on disbursal_date range
        filtered_applications = [
            app for app in mock_applications 
            if start_date <= app["disbursal_date"] <= end_date
        ]
        
        print(f"Table: Filtered applications count: {len(filtered_applications)}")
        
        if filtered_applications:
            base_data = {
                "applications": filtered_applications,
                "total_pages": 1,
                "current_page": 1,
                "total_items": len(filtered_applications)
            }
        else:
            # No data for selected date range
            base_data = {
                "applications": [],
                "total_pages": 0,
                "current_page": 1,
                "total_items": 0
            }
    else:
        # No date range provided, return all data
        base_data = {
            "applications": mock_applications,
            "total_pages": 1,
            "current_page": 1,
            "total_items": len(mock_applications)
        }
    
    return JsonResponse(base_data)

@csrf_exempt
def date_range(request):
    """API endpoint to get the available date range for disbursal data"""
    # Mock data - replace with your actual API call to get min/max dates
    # In production, this would query your database for the actual date range
    data = {
        "min_date": "2023-01-01",  # Replace with actual minimum date from your data
        "max_date": "2025-12-31",  # Replace with actual maximum date from your data
        "available_dates": [
            "2025-01-15",
            "2025-01-16", 
            "2025-01-17",
            "2025-01-18",
            "2025-01-19",
            "2025-01-20",
            "2025-01-21",
            "2025-01-22",
            "2025-01-23",
            "2025-01-24",
            "2025-01-25",
            "2025-01-26",
            "2025-01-27",
            "2025-01-28",
            "2025-01-29",
            "2025-01-30",
            "2025-01-31"
        ]
    }
    
    print(f"Date range requested - Min: {data['min_date']}, Max: {data['max_date']}")
    return JsonResponse(data)
