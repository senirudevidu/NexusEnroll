function showFields() {
    var role = document.getElementById('module').value;
    document.getElementById('studentFields').classList.add('hidden');
    document.getElementById('facultyFields').classList.add('hidden');
    if (role === 'student') {
        document.getElementById('studentFields').classList.remove('hidden');
    } else if (role === 'faculty') {
        document.getElementById('facultyFields').classList.remove('hidden');
    }
}