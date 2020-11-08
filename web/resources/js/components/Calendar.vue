<!-- Based on sample code from https://fullcalendar.io/docs/vue -->

<template>
    <FullCalendar :options="calendarOptions" />
</template>

<script>
    import FullCalendar from '@fullcalendar/vue';
    import dayGridPlugin from '@fullcalendar/daygrid';
    import interactionPlugin from '@fullcalendar/interaction';

    export default {
        components: {
            FullCalendar // to make the FullCalendar tag available
        },
        data() {
            return {
                calendarOptions: {
                    plugins: [dayGridPlugin, interactionPlugin],
                    interactionView: 'dayGridMonth'
                }
            };
        }
    }
</script>
