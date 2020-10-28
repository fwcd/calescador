<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class CreateEventUserTable extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        # Represents an attendance relation
        Schema::create('event_user', function (Blueprint $table) {
            $table->foreignId('user_id')->constrained();
            $table->foreignId('event_id')->constrained();
            $table->primary(['user_id', 'event_id']);
            $table->integer('count');
        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        Schema::dropIfExists('event_user');
    }
}
