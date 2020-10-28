<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Event extends Model
{
    use HasFactory;

    /**
     * The attributes that should be cast to native types.
     *
     * @var array
     */
    protected $casts = [
        'start_dt' => 'datetime',
        'end_dt' => 'datetime',
    ];

    /**
     * The attending users.
     */
    public function users()
    {
        return $this->belongsToMany('App\Models\User')->withPivot('count');
    }
}
