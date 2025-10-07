# vaccinations/utils_vaccine_display.py
from datetime import date, timedelta
from typing import List, Dict, Optional
from .models import Child, ChildDose, VaccineDose
from .utils import today

def compute_vaccine_display_status(child: Child, child_doses: List[ChildDose]) -> List[Dict]:
    """
    Compute vaccine display status according to IAP schedule requirements:
    - Show Complete Vaccine Schedule: Always visible
    - For Administered Vaccines: "Given on <Date>" in green
    - For Due Vaccines: "Due on <Date>" in red  
    - For Multi-Dose/Booster: Calculate based on previous dose or show "Previous dose pending"
    """
    today_date = today()
    
    # Create lookup for child doses by dose ID
    child_dose_map = {cd.dose_id: cd for cd in child_doses}
    
    # Get all vaccine doses for the schedule (should be from clinic_db/default)
    all_doses = list(VaccineDose.objects.using("default")
                    .select_related("vaccine", "previous_dose")
                    .order_by("min_offset_days", "vaccine__name", "sequence_index"))
    
    vaccine_rows = []
    
    for dose in all_doses:
        child_dose = child_dose_map.get(dose.id)
        
        # Basic vaccine info
        row = {
            'vaccine_name': dose.vaccine.name,
            'dose_label': dose.dose_label,
            'dose_id': dose.id,
            'sequence_index': dose.sequence_index,
            'is_booster': dose.is_booster,
            'min_offset_days': dose.min_offset_days,
            'max_offset_days': dose.max_offset_days,
        }
        
        # Determine status and styling
        if child_dose and child_dose.given_date:
            # ADMINISTERED: Show "Given on <Date>" in green
            row.update({
                'status': 'given',
                'status_text': f"Given on {child_dose.given_date.strftime('%d %b %Y')}",
                'status_class': 'text-success',
                'given_date': child_dose.given_date,
                'due_date': child_dose.due_date,
                'is_editable': False
            })
            
        elif dose.previous_dose_id:
            # BOOSTER/MULTI-DOSE: Check if previous dose is given
            previous_child_dose = child_dose_map.get(dose.previous_dose_id)
            
            if previous_child_dose and previous_child_dose.given_date:
                # Previous dose given - calculate due date for this dose
                calculated_due_date = previous_child_dose.given_date + timedelta(days=dose.min_offset_days)
                
                if calculated_due_date <= today_date:
                    # DUE: Show "Due on <Date>" in red
                    row.update({
                        'status': 'due',
                        'status_text': f"Due on {calculated_due_date.strftime('%d %b %Y')}",
                        'status_class': 'text-danger',
                        'due_date': calculated_due_date,
                        'is_editable': True
                    })
                else:
                    # FUTURE: Show "Due on <Date>" in blue
                    row.update({
                        'status': 'future',
                        'status_text': f"Due on {calculated_due_date.strftime('%d %b %Y')}",
                        'status_class': 'text-primary',
                        'due_date': calculated_due_date,
                        'is_editable': False
                    })
            else:
                # Previous dose not given - show "Previous dose pending"
                prev_vaccine_name = dose.previous_dose.vaccine.name if dose.previous_dose else "Previous dose"
                row.update({
                    'status': 'waiting_previous',
                    'status_text': f"Previous dose pending ({prev_vaccine_name})",
                    'status_class': 'text-muted',
                    'due_date': None,
                    'is_editable': False
                })
                
        else:
            # PRIMARY DOSE: Calculate based on birth date
            if child_dose and child_dose.due_date:
                due_date = child_dose.due_date
                
                if due_date <= today_date:
                    # DUE: Show "Due on <Date>" in red
                    row.update({
                        'status': 'due',
                        'status_text': f"Due on {due_date.strftime('%d %b %Y')}",
                        'status_class': 'text-danger',
                        'due_date': due_date,
                        'is_editable': True
                    })
                else:
                    # FUTURE: Show "Due on <Date>" in blue
                    row.update({
                        'status': 'future',
                        'status_text': f"Due on {due_date.strftime('%d %b %Y')}",
                        'status_class': 'text-primary',
                        'due_date': due_date,
                        'is_editable': False
                    })
            else:
                # No due date calculated
                row.update({
                    'status': 'not_scheduled',
                    'status_text': "Not scheduled",
                    'status_class': 'text-muted',
                    'due_date': None,
                    'is_editable': False
                })
        
        # Add overdue indicator for due vaccines
        if row.get('status') == 'due' and row.get('due_date'):
            days_overdue = (today_date - row['due_date']).days
            if days_overdue > 0:
                row['status_text'] += f" (Overdue by {days_overdue} days)"
                row['status_class'] = 'text-danger fw-bold'
        
        vaccine_rows.append(row)
    
    return vaccine_rows

def get_vaccine_summary_stats(vaccine_rows: List[Dict]) -> Dict:
    """Get summary statistics for vaccine status"""
    total = len(vaccine_rows)
    given = len([r for r in vaccine_rows if r.get('status') == 'given'])
    due = len([r for r in vaccine_rows if r.get('status') == 'due'])
    overdue = len([r for r in vaccine_rows if 'Overdue' in r.get('status_text', '')])
    pending = len([r for r in vaccine_rows if r.get('status') == 'waiting_previous'])
    
    return {
        'total': total,
        'given': given,
        'due': due,
        'overdue': overdue,
        'pending': pending,
        'completion_percentage': round((given / total * 100) if total > 0 else 0, 1)
    }
