<!-- Based on sample code from https://fullcalendar.io/docs/vue -->

<template>
    <FullCalendar :options="calendarOptions" />
</template>

<script>
    import FullCalendar from '@fullcalendar/vue';
    import dayGridPlugin from '@fullcalendar/daygrid';
    import interactionPlugin from '@fullcalendar/interaction';

    export default {
        props: ['events'],
        components: {
            FullCalendar // to make the FullCalendar tag available
        },
        data() {
            const events = JSON.parse(this.events);
            return {
                calendarOptions: {
                    plugins: [dayGridPlugin, interactionPlugin],
                    interactionView: 'dayGridMonth',
                    eventTimeFormat: {
                        hour: '2-digit',
                        minute: '2-digit',
                        hour12: false
                    },
                    events: events.map(e => ({
                        title: e.name,
                        start: e.start_dt,
                        end: e.end_dt
                    }))
                }
            };
        }
    }
</script>
