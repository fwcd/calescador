<?php

use App\Http\Controllers\ICSController;

/*
|--------------------------------------------------------------------------
| Calendar Routes
|--------------------------------------------------------------------------
|
| These routes are intended for specialized Calendar representations, e.g.
| iCalendar (.ics).
*/

// TODO: Require authentication on all routes
// TODO: User-specific calendars

Route::get('/all.ics', [ICSController::class, 'all']);
