# vaccinations/utils_due_vaccines.py
from datetime import date
from typing import List, Dict
from .models import Child, ChildDose, VaccineDose
from .utils import today

def get_due_vaccines_display(child: Child, child_doses: List[ChildDose]) -> List[Dict]:
    """
    Get vaccines that should be shown in 'Due Only' view:
    - All vaccines with due_date <= today
    - All vaccines that have been given (regardless of due date)
    - Show proper booster sequence and dependencies
    """
    today_date = today()
    
    # Create lookup for child doses by dose ID
    child_dose_map = {cd.dose_id: cd for cd in child_doses}
    
    # Get all vaccine doses ordered by timeline
    all_doses = list(VaccineDose.objects.using("default")
                    .select_related("vaccine", "previous_dose")
                    .order_by("min_offset_days", "vaccine__name", "sequence_index"))
    
    due_vaccine_rows = []
    
    for dose in all_doses:
        child_dose = child_dose_map.get(dose.id)
        
        # Skip if no child dose record
        if not child_dose:
            continue
        
        # Basic vaccine info
        row = {
            'vaccine_name': dose.vaccine.name,
            'dose_label': dose.dose_label,
            'dose_id': dose.id,
            'sequence_index': dose.sequence_index,
            'is_booster': dose.is_booster,
            'min_offset_days': dose.min_offset_days,
        }
        
        # Determine if this vaccine should be shown in "Due Only" view
        show_in_due_view = False
        
        if child_dose.given_date:
            # ALWAYS show given vaccines
            row.update({
                'status': 'given',
                'status_text': f"Given on {child_dose.given_date.strftime('%d %b %Y')}",
                'status_class': 'text-success fw-bold',
                'given_date': child_dose.given_date,
                'due_date': child_dose.due_date,
                'is_editable': False
            })
            show_in_due_view = True
            
        elif child_dose.due_date and child_dose.due_date <= today_date:
            # Show vaccines due today or overdue
            days_overdue = (today_date - child_dose.due_date).days
            
            if dose.previous_dose_id:
                # Check if previous dose is given
                previous_child_dose = child_dose_map.get(dose.previous_dose_id)
                
                if previous_child_dose and previous_child_dose.given_date:
                    # Previous dose given - this dose is ready
                    if days_overdue > 0:
                        row.update({
                            'status': 'overdue',
                            'status_text': f"Due on {child_dose.due_date.strftime('%d %b %Y')} (Overdue by {days_overdue} days)",
                            'status_class': 'text-danger fw-bold',
                            'due_date': child_dose.due_date,
                            'is_editable': True
                        })
                    else:
                        row.update({
                            'status': 'due',
                            'status_text': f"Due on {child_dose.due_date.strftime('%d %b %Y')}",
                            'status_class': 'text-danger',
                            'due_date': child_dose.due_date,
                            'is_editable': True
                        })
                    show_in_due_view = True
                else:
                    # Previous dose not given - show as waiting
                    prev_vaccine_name = dose.previous_dose.dose_label if dose.previous_dose else "Previous dose"
                    row.update({
                        'status': 'waiting_previous',
                        'status_text': f"Previous dose pending ({prev_vaccine_name})",
                        'status_class': 'text-muted',
                        'due_date': child_dose.due_date,
                        'is_editable': False
                    })
                    show_in_due_view = True  # Show waiting vaccines too
            else:
                # Primary dose - show if due
                if days_overdue > 0:
                    row.update({
                        'status': 'overdue',
                        'status_text': f"Due on {child_dose.due_date.strftime('%d %b %Y')} (Overdue by {days_overdue} days)",
                        'status_class': 'text-danger fw-bold',
                        'due_date': child_dose.due_date,
                        'is_editable': True
                    })
                else:
                    row.update({
                        'status': 'due',
                        'status_text': f"Due on {child_dose.due_date.strftime('%d %b %Y')}",
                        'status_class': 'text-danger',
                        'due_date': child_dose.due_date,
                        'is_editable': True
                    })
                show_in_due_view = True
        
        # Add to results if should be shown
        if show_in_due_view:
            due_vaccine_rows.append(row)
    
    return due_vaccine_rows

def get_vaccine_sequence_info(vaccine_name: str) -> Dict:
    """Get information about vaccine sequence and boosters"""
    sequences = {
        "DTwP/DTaP": {
            "total_doses": 5,
            "primary_series": 3,
            "boosters": 2,
            "schedule": "6 weeks, 10 weeks, 14 weeks, 16-18 months, 4-6 years"
        },
        "Hepatitis B": {
            "total_doses": 4,
            "primary_series": 1,
            "boosters": 3,
            "schedule": "Birth, 6 weeks, 10 weeks, 14 weeks"
        },
        "Hib": {
            "total_doses": 4,
            "primary_series": 3,
            "boosters": 1,
            "schedule": "6 weeks, 10 weeks, 14 weeks, 16-18 months"
        },
        "IPV": {
            "total_doses": 5,
            "primary_series": 3,
            "boosters": 2,
            "schedule": "6 weeks, 10 weeks, 14 weeks, 16-18 months, 4-6 years"
        }
    }
    
    return sequences.get(vaccine_name, {
        "total_doses": 1,
        "primary_series": 1,
        "boosters": 0,
        "schedule": "As per IAP guidelines"
    })
