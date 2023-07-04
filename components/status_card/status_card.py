from django_components import component


@component.register("status_card")
class Calendar(component.Component):
    template_name = "status_card/status_card.html"

    # This component takes one parameter, a date string to show in the template
    def get_context_data(self, head):
        return {
            "head": head,
        }
