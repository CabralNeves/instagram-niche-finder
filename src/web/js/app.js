const searchBtn = document.getElementById('searchBtn');
const searchListBtn = document.getElementById('searchListBtn');
const searchInput = document.getElementById('searchInput');
const loader = document.getElementById('loader');
const resultsGrid = document.getElementById('results');

searchBtn.addEventListener('click', async () => {
    const keyword = searchInput.value.trim();
    if (!keyword || keyword.length < 2) {
        alert('Por favor, digite um termo de busca válido.');
        return;
    }

    // Reset UI
    resultsGrid.innerHTML = '';
    loader.style.display = 'block';

    try {
        const response = await fetch(`/api/search?keyword=${encodeURIComponent(keyword)}`);
        const result = await response.json();

        if (result.status === 'success') {
            renderResults(result.data);
        } else {
            alert('Erro na busca: ' + result.detail);
        }
    } catch (error) {
        console.error('Error fetching data:', error);
        alert('Erro ao conectar com o servidor.');
    } finally {
        loader.style.display = 'none';
    }
});

searchListBtn.addEventListener('click', async () => {
    // Reset UI
    resultsGrid.innerHTML = '';
    loader.style.display = 'block';

    try {
        const response = await fetch('/api/search-list');
        const result = await response.json();

        if (result.status === 'success') {
            renderResults(result.data);
        } else {
            alert('Erro na busca: ' + result.detail);
        }
    } catch (error) {
        console.error('Error fetching data:', error);
        alert('Erro ao conectar com o servidor.');
    } finally {
        loader.style.display = 'none';
    }
});

function renderResults(profiles) {
    if (profiles.length === 0) {
        resultsGrid.innerHTML = '<p style="grid-column: 1/-1; text-align: center;">Nenhum perfil encontrado.</p>';
        return;
    }

    profiles.forEach(profile => {
        const card = document.createElement('div');
        card.className = 'card';
        
        card.innerHTML = `
            <div class="profile-header">
                <img src="${profile.profilePicUrl || 'https://via.placeholder.com/60'}" class="pic" alt="${profile.username}">
                <div>
                    <a href="${profile.url}" target="_blank" class="username">@${profile.username}</a>
                    <p style="margin: 0; font-size: 0.8rem; color: #8b949e;">${profile.fullName || ''}</p>
                </div>
            </div>
            <p style="font-size: 0.9rem; margin: 0;">${profile.biography ? profile.biography.substring(0, 100) + '...' : 'Sem bio.'}</p>
            <div class="stats">
                <div><span class="stat-val">${formatNumber(profile.followersCount)}</span> Seguidores</div>
                <div><span class="stat-val">${formatNumber(profile.postsCount)}</span> Posts</div>
            </div>
        `;
        resultsGrid.appendChild(card);
    });
}

function formatNumber(num) {
    if (!num) return '0';
    if (num >= 1000000) return (num / 1000000).toFixed(1) + 'M';
    if (num >= 1000) return (num / 1000).toFixed(1) + 'k';
    return num;
}
